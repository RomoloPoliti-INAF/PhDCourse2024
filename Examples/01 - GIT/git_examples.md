# Git Examples 


After the creation of a repository on GitHub:

1. Clone the repository in a local folder

```console
$ git clone
```

2. Add a new file, *tes.txt*, in the local folder then publish it in the remote repository:

```console
$ touch tes.txt
$ git add test.txt
$ git commit -m "First Commit"
$ git push
```

3. Create a branch of the repository called ***testing*** and add a new file called test2.txt to it:

```console
$ git branch testing
$ git checkout testing
$ touch test2.txt
$ git add *
$ git commit -m "Second Commit"
$ git push --set-upstream origin testing
```

4. Go back to the main repository and add the test3.txt file

```console
$ git switch main
$ touch test3.txt
$ git add *
$ git commit -m "Third Commit"
$ git push
```

5. Update the test.txt file on the *testing* branch

```console
$ git switch testing
$ echo "Linea di prova\n" >>test.txt
$ git status
$ git commit -a -m "Fourth Commit"
$ git push
$ git log --oneline --graph
```

6. Let's go back to the *branch* **main**. and merge it with the branch ***testing***, after which we add a file *test5.txt* and display the graph.

```console
$ git switch main
$ git merge testing
$ touch test6.txt
$ git add test6.txt
$ git commit -m "Sixth Commit"
$ git push
$ git log --oneline --graph
```