# Esempi GIT

Dopo aver creato il repository su gitHub:

1. Cloniamo il reporitory in un cartella locale
```console
$ git clone
```

2. Aggiungiamo un nuovo file, *tes.txt*, nella cartella locale e poi pubblichiamolo nel repository remoto

```console
$ touch tes.txt
$ git add test.txt
$ git commit -m "First Commit"
$ git push
```

3. Creiamo una ramificazione del repository chiamata ***testing*** a cui aggiungiamo un nuovo file chiamato test2.txt:

```console
$ git branch testing
$ git checkout testing
$ touch test2.txt
$ git add *
$ git commit -m "Second Commit"
$ git push --set-upstream origin testing
```

4. Ritorniamo al repository principale ed aggiungiamo il file test3.txt

```console
$ git switch main
$ touch test3.txt
$ git add *
$ git commit -m "Third Commit"
$ git push
```

5. Aggiorniamo il file test.txt sulla branch *testing*

```console
$ git switch testing
$ echo "Linea di prova\n" >>test.txt
$ git status
$ git commit -a -m "Fourth Commit"
$ git push
$ git log --oneline --graph
```

6. Torniamo nella *branch* **main**. e fondiamo questa con la branch ***testing***, dopo di che aggiungiamo un file *test5.txt* e visualizziamo il graficio.

```console
$ git switch main
$ git merge testing
$ touch test6.txt
$ git add test6.txt
$ git commit -m "Sixth Commit"
$ git push
$ git log --oneline --graph
```