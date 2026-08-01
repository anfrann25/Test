# Linux Challenges

Τα Linux challenges είναι μια σειρά από δέκα τοπικές ασκήσεις που σε βοηθούν να εξασκηθείς σε αρχεία, permissions, αναζήτηση, encoding, archives και βασική χρήση του terminal.

## Ασφαλής εκτέλεση

> Εκτέλεσέ τα μέσα σε Docker container ή disposable Virtual Machine. Μην τρέχεις το `setup.sh` στο κύριο λειτουργικό σου σύστημα χωρίς να έχεις πρώτα διαβάσει τον κώδικα.

## Εγκατάσταση σε Linux VM

Από τον βασικό φάκελο του project:

```bash
chmod +x src/setup.sh
sudo ./src/setup.sh
```

Το installer προσθέτει τα βοηθητικά commands και δημιουργεί τον λογαριασμό που χρειάζεται ένα από τα levels.

## Βασικές εντολές

Έλεγχος βαθμολογίας:

```bash
htb score
```

Προβολή προόδου:

```bash
htb progress
```

Υποβολή flag για Linux level:

```bash
htb redeem -m linux -l 1 -f YOUR_FLAG
```

Μηδενισμός προόδου:

```bash
htb reset
```

## Τι εξασκεί κάθε level

| Level | Κύρια δεξιότητα |
|---:|---|
| 1 | Ανάγνωση αρχείων |
| 2 | Εμφάνιση κρυφών αρχείων |
| 3 | Αναζήτηση μέσα σε noisy data |
| 4 | Εκτέλεση αρχείων και permissions |
| 5 | Αναγνώριση χρήσιμων στοιχείων |
| 6 | Encoding και transformations |
| 7 | Hidden data και input handling |
| 8 | Compressed archives |
| 9 | Hints και filesystem exploration |
| 10 | Users, authentication και τελικό challenge |

## Απεγκατάσταση

```bash
chmod +x src/uninstall.sh
sudo ./src/uninstall.sh
```

Το uninstall script αφαιρεί τα commands και τον εκπαιδευτικό system user που δημιούργησε το setup.
