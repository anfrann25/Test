#!/usr/bin/env python3
"""Cross-platform local companion for HackTheBasics.gr.

The website is educational only. This program runs locally to serve the academy,
show device-specific practice paths, and store lesson progress in the user's
profile. It uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

APP_NAME = "HackTheBasics Academy"
ROOT = Path(__file__).resolve().parent
CATALOG_FILE = ROOT / "academy_catalog.json"
STATE_DIR = Path.home() / ".hackthebasics"
STATE_FILE = STATE_DIR / "progress.json"


@dataclass(frozen=True)
class Device:
    key: str
    label: str
    python_command: str
    launcher: str


def detect_device() -> Device:
    prefix = os.environ.get("PREFIX", "").lower()
    if os.name == "nt":
        return Device("windows", "Windows", "py academy.py", "run-academy.bat")
    if "com.termux" in prefix or os.environ.get("TERMUX_VERSION") or os.environ.get("ANDROID_ROOT"):
        return Device("termux", "Android + Termux", "python academy.py", "./run-academy.sh")
    return Device("linux", f"Linux ({platform.system()} {platform.machine()})", "python3 academy.py", "./run-academy.sh")


def load_catalog() -> list[dict[str, Any]]:
    try:
        data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        lessons = data.get("lessons", [])
        if not isinstance(lessons, list):
            raise ValueError("Invalid catalog")
        return lessons
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Catalog error: {exc}", file=sys.stderr)
        return []


def default_state() -> dict[str, Any]:
    return {"version": 1, "language": "en", "completed": [], "last_lesson": None}


def load_state() -> dict[str, Any]:
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state = default_state()
        if isinstance(data, dict):
            state.update(data)
        if state.get("language") not in {"en", "el"}:
            state["language"] = "en"
        if not isinstance(state.get("completed"), list):
            state["completed"] = []
        return state
    except FileNotFoundError:
        return default_state()
    except (OSError, ValueError, json.JSONDecodeError):
        backup = STATE_FILE.with_suffix(".broken.json")
        try:
            if STATE_FILE.exists():
                shutil.copy2(STATE_FILE, backup)
        except OSError:
            pass
        return default_state()


def save_state(state: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    temporary = STATE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(STATE_FILE)


def text(state: dict[str, Any], en: str, el: str) -> str:
    return el if state.get("language") == "el" else en


def lesson_title(lesson: dict[str, Any], language: str) -> str:
    localized = lesson.get(language) or lesson.get("en") or {}
    return str(localized.get("title", lesson.get("id", "Unknown lesson")))


def find_lesson(catalog: list[dict[str, Any]], query: str) -> dict[str, Any] | None:
    query_lower = query.strip().lower()
    for lesson in catalog:
        if str(lesson.get("id", "")).lower() == query_lower:
            return lesson
    matches = [
        lesson for lesson in catalog
        if query_lower in lesson_title(lesson, "en").lower()
        or query_lower in lesson_title(lesson, "el").lower()
    ]
    return matches[0] if len(matches) == 1 else None


def show_banner(state: dict[str, Any], device: Device) -> None:
    print("=" * 66)
    print(f"{APP_NAME} — {device.label}")
    print(text(state,
               "Website: education only | Practice and progress: this device",
               "Ιστοσελίδα: μόνο εκπαίδευση | Πρακτική και πρόοδος: αυτή η συσκευή"))
    print("=" * 66)


def show_status(state: dict[str, Any], catalog: list[dict[str, Any]], device: Device) -> None:
    completed = set(str(item) for item in state.get("completed", []))
    known = {str(item.get("id")) for item in catalog}
    count = len(completed & known)
    total = len(catalog)
    percent = round((count / total) * 100) if total else 0
    show_banner(state, device)
    print(text(state, "Completed lessons", "Ολοκληρωμένα μαθήματα") + f": {count}/{total} ({percent}%)")
    print(text(state, "Progress file", "Αρχείο προόδου") + f": {STATE_FILE}")
    if state.get("last_lesson"):
        lesson = find_lesson(catalog, str(state["last_lesson"]))
        if lesson:
            print(text(state, "Last lesson", "Τελευταίο μάθημα") + f": {lesson_title(lesson, state['language'])}")


def list_lessons(state: dict[str, Any], catalog: list[dict[str, Any]], only_pending: bool = False) -> None:
    completed = set(str(item) for item in state.get("completed", []))
    language = state.get("language", "en")
    for number, lesson in enumerate(catalog, 1):
        lesson_id = str(lesson.get("id"))
        done = lesson_id in completed
        if only_pending and done:
            continue
        mark = "✓" if done else "·"
        print(f"{mark} {number:02d}. {lesson_title(lesson, language)} [{lesson_id}]")


def complete_lesson(state: dict[str, Any], catalog: list[dict[str, Any]], query: str, done: bool = True) -> bool:
    lesson = find_lesson(catalog, query)
    if not lesson:
        print(text(state, "Lesson not found. Use 'lessons' to see IDs.", "Το μάθημα δεν βρέθηκε. Χρησιμοποίησε 'lessons' για τα IDs."), file=sys.stderr)
        return False
    lesson_id = str(lesson["id"])
    completed = set(str(item) for item in state.get("completed", []))
    if done:
        completed.add(lesson_id)
        state["last_lesson"] = lesson_id
    else:
        completed.discard(lesson_id)
    state["completed"] = sorted(completed)
    save_state(state)
    action = text(state, "Completed", "Ολοκληρώθηκε") if done else text(state, "Reopened", "Άνοιξε ξανά")
    print(f"{action}: {lesson_title(lesson, state['language'])}")
    return True


def device_paths(state: dict[str, Any], device: Device) -> None:
    show_banner(state, device)
    print(text(state, "Project directory", "Φάκελος project") + f": {ROOT}")
    print(text(state, "Educational website", "Εκπαιδευτική ιστοσελίδα") + f": {ROOT / 'home.html'}")
    print(text(state, "Python challenges", "Python challenges") + f": {ROOT / 'labs/python/python_challenges'}")
    if device.key == "termux":
        print(text(state, "Portable shell material", "Φορητό shell υλικό") + f": {ROOT / 'labs/linux/linux_challenges'}")
        print(text(state,
                   "Note: bundled x86-64 binaries usually do not run on ARM Android.",
                   "Σημείωση: τα x86-64 binaries συνήθως δεν τρέχουν σε ARM Android."))
    else:
        print(text(state, "Linux challenges", "Linux challenges") + f": {ROOT / 'labs/linux/linux_challenges'}")
    print(text(state, "Command-line tools", "Εργαλεία command line") + f": {ROOT / 'tools/htb-cli'}")


def available_port(preferred: int) -> int:
    for port in range(preferred, preferred + 25):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise OSError("No available local port found")


def open_url(url: str, device: Device) -> None:
    if device.key == "termux" and shutil.which("termux-open-url"):
        try:
            import subprocess
            subprocess.Popen(["termux-open-url", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except OSError:
            pass
    try:
        webbrowser.open(url)
    except Exception:
        pass


def serve(state: dict[str, Any], device: Device, port: int, no_browser: bool = False) -> None:
    port = available_port(port)
    url = f"http://127.0.0.1:{port}/home.html"

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            print(f"[web] {format % args}")

    old_cwd = Path.cwd()
    os.chdir(ROOT)
    server = ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    print(text(state, "Educational academy running at", "Η εκπαιδευτική ακαδημία τρέχει στο") + f": {url}")
    print(text(state,
               "The website does not execute terminal commands. Press Ctrl+C to stop.",
               "Η ιστοσελίδα δεν εκτελεί εντολές terminal. Πάτησε Ctrl+C για διακοπή."))
    if not no_browser:
        threading.Thread(target=lambda: (time.sleep(0.5), open_url(url, device)), daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n" + text(state, "Academy server stopped.", "Ο server της ακαδημίας σταμάτησε."))
    finally:
        server.server_close()
        os.chdir(old_cwd)


def set_language(state: dict[str, Any], language: str) -> None:
    if language not in {"en", "el"}:
        raise ValueError("Language must be en or el")
    state["language"] = language
    save_state(state)
    print("Language: " + ("Ελληνικά" if language == "el" else "English"))


def reset_progress(state: dict[str, Any], assume_yes: bool = False) -> None:
    if not assume_yes:
        prompt = text(state, "Delete all local academy progress? [y/N]: ", "Διαγραφή όλης της τοπικής προόδου; [y/N]: ")
        if input(prompt).strip().lower() not in {"y", "yes", "ν", "ναι"}:
            print(text(state, "Cancelled.", "Ακυρώθηκε."))
            return
    state["completed"] = []
    state["last_lesson"] = None
    save_state(state)
    print(text(state, "Local progress reset.", "Η τοπική πρόοδος μηδενίστηκε."))


def interactive(state: dict[str, Any], catalog: list[dict[str, Any]], device: Device) -> None:
    while True:
        show_status(state, catalog, device)
        print()
        options = [
            text(state, "Start educational website locally", "Εκκίνηση εκπαιδευτικής ιστοσελίδας τοπικά"),
            text(state, "List lessons", "Λίστα μαθημάτων"),
            text(state, "Mark a lesson complete", "Σήμανση μαθήματος ως ολοκληρωμένο"),
            text(state, "Reopen a lesson", "Επαναφορά μαθήματος"),
            text(state, "Show local practice paths", "Εμφάνιση τοπικών paths πρακτικής"),
            text(state, "Change language", "Αλλαγή γλώσσας"),
            text(state, "Reset local progress", "Μηδενισμός τοπικής προόδου"),
        ]
        for index, option in enumerate(options, 1):
            print(f"[{index}] {option}")
        print("[0] " + text(state, "Exit", "Έξοδος"))
        choice = input("> ").strip()
        if choice == "0":
            return
        if choice == "1":
            serve(state, device, 8000)
        elif choice == "2":
            list_lessons(state, catalog)
            input(text(state, "Press Enter to continue…", "Πάτησε Enter για συνέχεια…"))
        elif choice in {"3", "4"}:
            list_lessons(state, catalog, only_pending=choice == "3")
            query = input(text(state, "Lesson ID or unique title: ", "ID μαθήματος ή μοναδικός τίτλος: ")).strip()
            complete_lesson(state, catalog, query, done=choice == "3")
        elif choice == "5":
            device_paths(state, device)
            input(text(state, "Press Enter to continue…", "Πάτησε Enter για συνέχεια…"))
        elif choice == "6":
            set_language(state, "el" if state.get("language") == "en" else "en")
        elif choice == "7":
            reset_progress(state)
        else:
            print(text(state, "Invalid option.", "Μη έγκυρη επιλογή."))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local companion for the HackTheBasics educational academy.")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("status", help="Show local progress and detected device")
    lessons = sub.add_parser("lessons", help="List academy lessons and local completion state")
    lessons.add_argument("--pending", action="store_true", help="Show only incomplete lessons")
    complete = sub.add_parser("complete", help="Mark a lesson complete in the local profile")
    complete.add_argument("lesson")
    reopen = sub.add_parser("reopen", help="Remove a lesson from local completion")
    reopen.add_argument("lesson")
    sub.add_parser("paths", help="Show local practice directories for this device")
    serve_parser = sub.add_parser("serve", help="Serve the educational website locally")
    serve_parser.add_argument("--port", type=int, default=8000)
    serve_parser.add_argument("--no-browser", action="store_true")
    language = sub.add_parser("language", help="Set interface language")
    language.add_argument("value", choices=["en", "el"])
    reset = sub.add_parser("reset", help="Reset local program progress")
    reset.add_argument("--yes", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    device = detect_device()
    catalog = load_catalog()
    state = load_state()

    if not args.command:
        interactive(state, catalog, device)
    elif args.command == "status":
        show_status(state, catalog, device)
    elif args.command == "lessons":
        list_lessons(state, catalog, args.pending)
    elif args.command == "complete":
        return 0 if complete_lesson(state, catalog, args.lesson, True) else 1
    elif args.command == "reopen":
        return 0 if complete_lesson(state, catalog, args.lesson, False) else 1
    elif args.command == "paths":
        device_paths(state, device)
    elif args.command == "serve":
        serve(state, device, args.port, args.no_browser)
    elif args.command == "language":
        set_language(state, args.value)
    elif args.command == "reset":
        reset_progress(state, args.yes)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
