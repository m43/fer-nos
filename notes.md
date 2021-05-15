# Ma notes

<!-- ✘✓ -->

## Lab 1

A useful command:

```sh
watch -n 0.7 -t 'ipcs -q'
```

### Zadatak A - Radovi na cesti

> Stari most je uski most i stoga postavlja ograničenja na promet. Na njemu istovremeno smije biti najviše 3 automobila koji voze u istom smjeru. Simulirati automobile procesom Auto koji obavlja niže navedene radnje. Napisati program koji stvara N automobila, gdje je N proizvoljan broj između 5 i 100 koji se određuje prilikom pokretanja programa te svakom automobilu dodjeljuje registarsku oznaku. Smjer se automobilu određuje nasumično.

✓

> Proces semafor određuje koji automobili će prijeći most, a početni smjer prijelaza se određuje nasumično te se zatim izmjenjuju. Prijelazak mosta se omogućuje kada se zabilježi 3 zahtjeva za prijelaz u trenutnom smjeru ili prođe X milisekundi, gdje je X slučajan broj između 500 i 1000. Prijelaz mosta traje Y milisekundi gdje je Y broj između 1000 i 3000.

✓

> Procesi međusobno komuniciraju uz pomoć reda poruka koristeći raspodijeljeni centralizirani protokol, gdje je proces Semafor odgovoran za međusobno isključivanje.

Za raspodijeljeni centralizirani protokol sam izmislio neki koji radi s tri reda poruka s jednim centralnim čvorom (centralni čvor zovem semafor, implementiran je u a_semaphore.c). Nisam implementirao neki od protokola obrađenih na predavanjima kao na primjer Lamportov protokol.

```c
Proces Auto(registarska_oznaka, smjer) {
   // smjer = 0 ili 1
   // registarska oznaka je redni broj automobila u sustavu
   spavaj Z milisekundi; // Z je slučajan broj između 100 i 2000
   pošalji zahtjev za prijelaz mosta i ispiši("Automobil registarska_oznaka čeka na prelazak preko mosta");
   po primitku poruke "Prijeđi" ispiši("Automobil registarska_oznaka se popeo na most");
   po primitku poruke "Prešao" ispiši("Automobil registarska_oznaka je prešao most.");
}
```

> Napomene:
>
> - Obavezno komentirati izvorni tekst programa (programski kod).
> - Sve što u zadatku nije zadano, riješiti na proizvoljan način.

Nisam htio pretjerati s komentarima.

<details>
  <summary>Primjer konačnog ispisa:</summary>

```js
[user72@user72pc lab1]$ ./a_run.sh 
Compile a_entry

Compile a_semaphore
a_semaphore.c: In function ‘main’:
a_semaphore.c:12:5: warning: implicit declaration of function ‘sigset’ [-Wimplicit-function-declaration]
   12 |     sigset(SIGINT, retreat); // If interupted, queues must be closed!
      |     ^~~~~~

Compile a_car

Compiling done. Gonna run a_entry

Entry: Lab 1a demo started.
Entry: will create 30 cars
Traffic semaphore started
Semaphore: saw registration 1
Car <--- 1 waiting for the ticket
Semaphore: saw registration 2
Car ---> 2 waiting for the ticket
Semaphore: saw registration 6
Car <--- 6 waiting for the ticket
Semaphore: saw registration 5
Car ---> 5 waiting for the ticket
Semaphore: saw registration 4
Car ---> 4 waiting for the ticket
Car <--- 10 waiting for the ticket
Car <--- 12 waiting for the ticket
Car <--- 9 waiting for the ticket
Car <--- 8 waiting for the ticket
Car <--- 3 waiting for the ticket
Car ---> 11 waiting for the ticket
Car <--- 7 waiting for the ticket
Car <--- 14 waiting for the ticket
Car ---> 13 waiting for the ticket
Car <--- 20 waiting for the ticket
Car <--- 22 waiting for the ticket
Car ---> 24 waiting for the ticket
Car <--- 18 waiting for the ticket
Car ---> 17 waiting for the ticket
Car <--- 15 waiting for the ticket
Car ---> 23 waiting for the ticket
Car <--- 28 waiting for the ticket
Car ---> 27 waiting for the ticket
Car <--- 30 waiting for the ticket
Car ---> 26 waiting for the ticket
Car <--- 21 waiting for the ticket
Car ---> 25 waiting for the ticket
Car <--- 16 waiting for the ticket
Car <--- 29 waiting for the ticket
Car <--- 19 waiting for the ticket
Semaphore - time elapsed: 00988ms
Semaphore: sending ticket to 2
Semaphore: sending ticket to 5
Semaphore: sending ticket to 4
Car ---> 5 crossing the bridge
Car ---> 2 crossing the bridge
Car ---> 4 crossing the bridge
Car ---> 5 crossed the bridge
Semaphore: collected car 5
Car ---> 4 crossed the bridge
Car ---> 2 crossed the bridge
Semaphore: collected car 4
Semaphore: collected car 2
Semaphore: collected all cars. nice
Semaphore: saw registration 10
Semaphore - time elapsed: 00702ms
Semaphore: sending ticket to 1
Semaphore: sending ticket to 6
Semaphore: sending ticket to 10
Car <--- 6 crossing the bridge
Car <--- 10 crossing the bridge
Car <--- 1 crossing the bridge
Car <--- 1 crossed the bridge
Car <--- 6 crossed the bridge
Car <--- 10 crossed the bridge
Semaphore: collected car 10
Semaphore: collected car 1
Semaphore: collected car 6
Semaphore: collected all cars. nice
Semaphore: saw registration 12
Semaphore: saw registration 9
Semaphore: saw registration 8
Semaphore - time elapsed: 00898ms
Semaphore: sending ticket to 12
Semaphore: sending ticket to 9
Semaphore: sending ticket to 8
Car <--- 8 crossing the bridge
Car <--- 12 crossing the bridge
Car <--- 9 crossing the bridge
Car <--- 9 crossed the bridge
Car <--- 8 crossed the bridge
Car <--- 12 crossed the bridge
Semaphore: collected car 9
Semaphore: collected car 8
Semaphore: collected car 12
Semaphore: collected all cars. nice
Semaphore: saw registration 3
Semaphore: saw registration 11
Semaphore: saw registration 7
Semaphore: saw registration 14
Semaphore - time elapsed: 00960ms
Semaphore: sending ticket to 3
Semaphore: sending ticket to 7
Semaphore: sending ticket to 14
Car <--- 3 crossing the bridge
Car <--- 7 crossing the bridge
Car <--- 14 crossing the bridge
Car <--- 14 crossed the bridge
Car <--- 7 crossed the bridge
Car <--- 3 crossed the bridge
Semaphore: collected car 7
Semaphore: collected car 14
Semaphore: collected car 3
Semaphore: collected all cars. nice
Semaphore: saw registration 13
Semaphore: saw registration 20
Semaphore: saw registration 15
Semaphore: saw registration 24
Semaphore - time elapsed: 00651ms
Semaphore: sending ticket to 11
Semaphore: sending ticket to 13
Semaphore: sending ticket to 24
Car ---> 24 crossing the bridge
Car ---> 13 crossing the bridge
Car ---> 11 crossing the bridge
Car ---> 24 crossed the bridge
Car ---> 13 crossed the bridge
Car ---> 11 crossed the bridge
Semaphore: collected car 11
Semaphore: collected car 24
Semaphore: collected car 13
Semaphore: collected all cars. nice
Semaphore: saw registration 22
Semaphore - time elapsed: 00639ms
Semaphore: sending ticket to 20
Semaphore: sending ticket to 15
Semaphore: sending ticket to 22
Car <--- 15 crossing the bridge
Car <--- 22 crossing the bridge
Car <--- 20 crossing the bridge
Car <--- 15 crossed the bridge
Semaphore: collected car 15
Car <--- 22 crossed the bridge
Car <--- 20 crossed the bridge
Semaphore: collected car 22
Semaphore: collected car 20
Semaphore: collected all cars. nice
Semaphore: saw registration 18
Semaphore: saw registration 17
Semaphore: saw registration 23
Semaphore: saw registration 28
Semaphore: saw registration 30
Semaphore - time elapsed: 00976ms
Semaphore: sending ticket to 18
Semaphore: sending ticket to 28
Semaphore: sending ticket to 30
Car <--- 30 crossing the bridge
Car <--- 18 crossing the bridge
Car <--- 28 crossing the bridge
Car <--- 30 crossed the bridge
Car <--- 18 crossed the bridge
Car <--- 28 crossed the bridge
Semaphore: collected car 30
Semaphore: collected car 28
Semaphore: collected car 18
Semaphore: collected all cars. nice
Semaphore: saw registration 27
Semaphore - time elapsed: 00675ms
Semaphore: sending ticket to 17
Semaphore: sending ticket to 23
Semaphore: sending ticket to 27
Car ---> 17 crossing the bridge
Car ---> 23 crossing the bridge
Car ---> 27 crossing the bridge
Car ---> 17 crossed the bridge
Car ---> 23 crossed the bridge
Car ---> 27 crossed the bridge
Semaphore: collected car 17
Semaphore: collected car 23
Semaphore: collected car 27
Semaphore: collected all cars. nice
Semaphore: saw registration 26
Semaphore: saw registration 21
Semaphore: saw registration 25
Semaphore: saw registration 16
Semaphore: saw registration 29
Semaphore - time elapsed: 00973ms
Semaphore: sending ticket to 21
Semaphore: sending ticket to 16
Semaphore: sending ticket to 29
Car <--- 29 crossing the bridge
Car <--- 16 crossing the bridge
Car <--- 21 crossing the bridge
Car <--- 21 crossed the bridge
Car <--- 16 crossed the bridge
Car <--- 29 crossed the bridge
Semaphore: collected car 29
Semaphore: collected car 16
Semaphore: collected car 21
Semaphore: collected all cars. nice
Semaphore: saw registration 19
Semaphore - time elapsed: 00672ms
Semaphore: sending ticket to 26
Semaphore: sending ticket to 25
Car ---> 26 crossing the bridge
Car ---> 25 crossing the bridge
Car ---> 25 crossed the bridge
Car ---> 26 crossed the bridge
Semaphore: collected car 26
Semaphore: collected car 25
Semaphore: collected all cars. nice
Semaphore - time elapsed: 00502ms
Semaphore: sending ticket to 19
Car <--- 19 crossing the bridge
Car <--- 19 crossed the bridge
Semaphore: collected car 19
Semaphore: collected all cars. nice
Semaphore - time elapsed: 10000ms
Traffic semaphore quit. Collected 30 cars in total.
Entry: Lab 1a demo finished.
```

</details>


### Zadatak B - Baza podataka

> Pretpostavimo da u sustavu imamo N procesa i jednu bazu podataka (u ovom slučaju baza se simulira nizom struktura podataka) koja za svaki proces struktura podataka procesa sadrži identifikator procesa, vrijednost logičkog sata procesa te broj ulazaka u kritički odsječak procesa. Neka je baza podataka dijeljena između procesa na način da je promjena vrijednosti od strane jednog procesa vidljiva svim ostalim procesima. Pristup bazi podataka predstavlja kritički odsječak: najviše jedan proces u svakom trenutku može biti u kritičkom odsječku. Unutar kritičkog odsječka, svaki proces ponavlja 5 puta sljedeće radnje.
>
> 1. U bazi podataka, ažurira svoju vrijednost logičkog sata trenutnom i inkrementira svoj broj ulazaka u kritički odsječak.
> 2. Ispiše sadržaj cijele (ne samo svog unosa) baze podataka na standardni izlaz.
> 3. Spava X milisekundi gdje je X je slučajan broj između 100 i 2000

✓

Tokom spavanja, moji procesi nisu responzivni. Blokiranu su.

> Na početku glavni proces stvara N  procesa (broj N se zadaje i može biti u intervalu [3,10]) koji dalje međusobno komuniciraju običnim ili imenovanim cjevovodima (svejedno). Sinkronizirajte pristupanje bazi podataka koristeći
>
> - Lamportov raspodijeljeni protokol (rješavaju studenti čija je zadnja znamenka JMBAG parna) ili
> - protokol Ricarta i Agrawala (rješavaju studenti čija je zadnja znamenka JMBAG neparna).

Implementirao sam R&A algoritam tako da svaki proces radi X ciklusa pristupa kritičnom odsječku. Ciklus završava izlaskom iz K.O. i obavještavanjem procesa koji čekaju odgovor, a odmah potom počinje novi ciklus gdje proces spava tako da se blokira na nasumičnu količinu vremena. Nakon što se proces probudi, on **ne gleda** ima li zahtjeva od drugih procesa za ulaskom u K.O., nego prvo pošalje svoj zahtjev za novi ulazak u K.O. i tek onda pokreće petlju u kojoj obrađuje zahtjeve i odgovore.

Zbog toga je kod napisane implementacije očekivano da će zbog ovakvih cikličkih zahtjeva za pristup kritičnom odsječku svi procesi, ako su na početku imali svi jednake vrijednosti, imati istu vrijednost lokalnog logičkog sata nakon što završi bilo koji ciklus. Kako tada procesi na početku svakog ciklusa imaju jednaku vrijednost lokalnog logičkog sata, tako će se svaki put sinkronizirati tako da proces s najvišim indeksom (jer njemu dajem prednost) uđe u K.O. I doista ako se postave svi logički satovi na istu vrijednost, onda će oni uvijek ulaziti istim redoslijedom u K.O. (od posljednjeg procesa prema prvom) i imati iste vrijednosti logičkih satova nakon završetka bilo kojeg ciklusa.

Ako su inicijalne vrijednosti logičkih satova postavljene nasumično, one će se djelomično istitrati nakon prvih ciklusa, ali ne moraju slijediti isto ponašanje koje je prethodno opisano.

Nakon što završe svi ciklusi, procesi ne spavaju nego jedan dio vremena obrađuju nadolazeće zahtjeve i jedan dio vremena spavaju. Nakon što je prošlo Y sekundi bez ijednog novog zahtjeva, proces se gasi i mota kablove.

> Napomene:
>
> - Bazu podataka možete definirati kao "struct db_entry database[N]".
> - Za dijeljenje baze podataka između procesa koristiti zajednički spremnik (sustavski pozive mmap ili shmat).
> - Svi procesi ispisuju poruku koju šalju i poruku koju primaju.
> - Obavezno komentirati izvorni tekst programa (programski kod).
> - Sve što u zadatku nije zadano, riješiti na proizvoljan način.

Koristio sam mmap. Procesi ispisuju poruke ako je uključena globalna zastavica DEBUG.

<details>
  <summary>Konačni ispis za n=4 procesa bez debuga:</summary>

```js
Main: Lab 1b demo started.
Main: will create 4 processes
pid=2: database at local_logical_time=29
pid:00 logclk:0000 c:0
pid:01 logclk:0000 c:0
pid:02 logclk:0029 c:1
pid:03 logclk:0000 c:0

pid=3: database at local_logical_time=29
pid:00 logclk:0000 c:0
pid:01 logclk:0000 c:0
pid:02 logclk:0029 c:1
pid:03 logclk:0029 c:1

pid=1: database at local_logical_time=29
pid:00 logclk:0000 c:0
pid:01 logclk:0029 c:1
pid:02 logclk:0029 c:1
pid:03 logclk:0029 c:1

pid=0: database at local_logical_time=29
pid:00 logclk:0029 c:1
pid:01 logclk:0029 c:1
pid:02 logclk:0029 c:1
pid:03 logclk:0029 c:1

pid=3: database at local_logical_time=35
pid:00 logclk:0029 c:1
pid:01 logclk:0029 c:1
pid:02 logclk:0029 c:1
pid:03 logclk:0035 c:2

pid=2: database at local_logical_time=35
pid:00 logclk:0029 c:1
pid:01 logclk:0029 c:1
pid:02 logclk:0035 c:2
pid:03 logclk:0035 c:2

pid=1: database at local_logical_time=35
pid:00 logclk:0029 c:1
pid:01 logclk:0035 c:2
pid:02 logclk:0035 c:2
pid:03 logclk:0035 c:2

pid=0: database at local_logical_time=35
pid:00 logclk:0035 c:2
pid:01 logclk:0035 c:2
pid:02 logclk:0035 c:2
pid:03 logclk:0035 c:2

pid=3: database at local_logical_time=41
pid:00 logclk:0035 c:2
pid:01 logclk:0035 c:2
pid:02 logclk:0035 c:2
pid:03 logclk:0041 c:3

pid=2: database at local_logical_time=41
pid:00 logclk:0035 c:2
pid:01 logclk:0035 c:2
pid:02 logclk:0041 c:3
pid:03 logclk:0041 c:3

pid=1: database at local_logical_time=41
pid:00 logclk:0035 c:2
pid:01 logclk:0041 c:3
pid:02 logclk:0041 c:3
pid:03 logclk:0041 c:3

pid=0: database at local_logical_time=41
pid:00 logclk:0041 c:3
pid:01 logclk:0041 c:3
pid:02 logclk:0041 c:3
pid:03 logclk:0041 c:3

pid=3: database at local_logical_time=47
pid:00 logclk:0041 c:3
pid:01 logclk:0041 c:3
pid:02 logclk:0041 c:3
pid:03 logclk:0047 c:4

pid=2: database at local_logical_time=47
pid:00 logclk:0041 c:3
pid:01 logclk:0041 c:3
pid:02 logclk:0047 c:4
pid:03 logclk:0047 c:4

pid=1: database at local_logical_time=47
pid:00 logclk:0041 c:3
pid:01 logclk:0047 c:4
pid:02 logclk:0047 c:4
pid:03 logclk:0047 c:4

pid=0: database at local_logical_time=47
pid:00 logclk:0047 c:4
pid:01 logclk:0047 c:4
pid:02 logclk:0047 c:4
pid:03 logclk:0047 c:4

pid=3: database at local_logical_time=53
pid:00 logclk:0047 c:4
pid:01 logclk:0047 c:4
pid:02 logclk:0047 c:4
pid:03 logclk:0053 c:5

pid=2: database at local_logical_time=53
pid:00 logclk:0047 c:4
pid:01 logclk:0047 c:4
pid:02 logclk:0053 c:5
pid:03 logclk:0053 c:5

pid=1: database at local_logical_time=53
pid:00 logclk:0047 c:4
pid:01 logclk:0053 c:5
pid:02 logclk:0053 c:5
pid:03 logclk:0053 c:5

pid=0: database at local_logical_time=53
pid:00 logclk:0053 c:5
pid:01 logclk:0053 c:5
pid:02 logclk:0053 c:5
pid:03 logclk:0053 c:5

pid=3: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 53
pid=2: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 53
pid=1: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 53
pid=0: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 53
Main: Lab 1b demo finished.

Process finished with exit code 0
```

</details>

<details>
  <summary>Konačni ispis za n=4 procesa s debugom:</summary>

```js
Main: Lab 1b demo started.
Main: will create 4 processes
0-->1, 6 in f2048   0-->1, 7 out f1
0-->2, 8 in f2048   0-->2, 9 out f1
0-->3, 10 in f2048   0-->3, 11 out f1
1-->0, 12 in f2048   1-->0, 19 out f1
1-->2, 20 in f2048   1-->2, 21 out f1
1-->3, 22 in f2048   1-->3, 23 out f1
2-->0, 24 in f2048   2-->0, 25 out f1
2-->1, 26 in f2048   2-->1, 27 out f1
2-->3, 34 in f2048   2-->3, 35 out f1
3-->0, 36 in f2048   3-->0, 37 out f1
3-->1, 44 in f2048   3-->1, 45 out f1
3-->2, 46 in f2048   3-->2, 61 out f1
pid=0: Started
pid=0: Gonna sleep now.
pid=1: Started
pid=1: Gonna sleep now.
pid=2: Started
pid=2: Gonna sleep now.
pid=3: Started
pid=3: Gonna sleep now.
pid=0: I want to use the database
pid=0: Waiting for responses
pid=3: I want to use the database
pid=3: Waiting for responses
pid=3: New message in inbox from 0, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 0, its a response
pid=3: Got 1 responses and 1 pids to notify
pid=1: I want to use the database
pid=1: Waiting for responses
pid=1: New message in inbox from 0, its a request
pid=1: I'll notify him later on
pid=1: Got 0 responses and 1 pids to notify
pid=1: New message in inbox from 3, its a request
pid=1: Told him to go ahead
pid=1: Got 0 responses and 1 pids to notify
pid=0: New message in inbox from 1, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 1, its a request
pid=3: I'll notify him later on
pid=3: Got 1 responses and 2 pids to notify
pid=1: New message in inbox from 0, its a response
pid=1: Got 1 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a response
pid=3: Got 2 responses and 2 pids to notify
pid=2: I want to use the database
pid=2: Waiting for responses
pid=2: New message in inbox from 0, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 1 pids to notify
pid=2: New message in inbox from 1, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 2 pids to notify
pid=2: New message in inbox from 3, its a request
pid=2: Told him to go ahead
pid=2: Got 0 responses and 2 pids to notify
pid=1: New message in inbox from 2, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 2, its a request
pid=3: I'll notify him later on
pid=3: Got 2 responses and 3 pids to notify
pid=2: New message in inbox from 0, its a response
pid=2: Got 1 responses and 2 pids to notify
pid=2: New message in inbox from 1, its a response
pid=2: Got 2 responses and 2 pids to notify
pid=3: New message in inbox from 2, its a response
pid=3: Got 3 responses and 3 pids to notify
pid=3: Got all responses
pid=3: database at local_logical_time=6
pid:00 logclk:0000 c:0
pid:01 logclk:0000 c:0
pid:02 logclk:0000 c:0
pid:03 logclk:0006 c:1
pid=3: Done with critical code. Gonna notify 3 processes now
pid=3: Notified everybody.
pid=3: Gonna sleep now.
pid=2: New message in inbox from 3, its a response
pid=2: Got 3 responses and 2 pids to notify
pid=1: New message in inbox from 3, its a response
pid=1: Got 2 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a response
pid=0: Got 1 responses and 0 pids to notify
pid=2: Got all responses
pid=2: database at local_logical_time=6
pid:00 logclk:0000 c:0
pid:01 logclk:0000 c:0
pid:02 logclk:0006 c:1
pid:03 logclk:0006 c:1
pid=2: Done with critical code. Gonna notify 2 processes now
pid=2: Notified everybody.
pid=2: Gonna sleep now.
pid=1: New message in inbox from 2, its a response
pid=1: Got 3 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a response
pid=0: Got 2 responses and 0 pids to notify
pid=1: Got all responses
pid=1: database at local_logical_time=6
pid:00 logclk:0000 c:0
pid:01 logclk:0006 c:1
pid:02 logclk:0006 c:1
pid:03 logclk:0006 c:1
pid=1: Done with critical code. Gonna notify 1 processes now
pid=1: Notified everybody.
pid=1: Gonna sleep now.
pid=0: New message in inbox from 1, its a response
pid=0: Got 3 responses and 0 pids to notify
pid=0: Got all responses
pid=0: database at local_logical_time=6
pid:00 logclk:0006 c:1
pid:01 logclk:0006 c:1
pid:02 logclk:0006 c:1
pid:03 logclk:0006 c:1
pid=0: Done with critical code. Gonna notify 0 processes now
pid=0: Notified everybody.
pid=0: Gonna sleep now.
pid=0: I want to use the database
pid=0: Waiting for responses
pid=1: I want to use the database
pid=1: Waiting for responses
pid=1: New message in inbox from 0, its a request
pid=1: I'll notify him later on
pid=1: Got 0 responses and 1 pids to notify
pid=0: New message in inbox from 1, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=1: New message in inbox from 0, its a response
pid=1: Got 1 responses and 1 pids to notify
pid=2: I want to use the database
pid=2: Waiting for responses
pid=2: New message in inbox from 0, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 1 pids to notify
pid=2: New message in inbox from 1, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 2 pids to notify
pid=1: New message in inbox from 2, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=2: New message in inbox from 0, its a response
pid=2: Got 1 responses and 2 pids to notify
pid=2: New message in inbox from 1, its a response
pid=2: Got 2 responses and 2 pids to notify
pid=3: I want to use the database
pid=3: Waiting for responses
pid=3: New message in inbox from 0, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 2 pids to notify
pid=3: New message in inbox from 2, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 3 pids to notify
pid=1: New message in inbox from 3, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=2: New message in inbox from 3, its a request
pid=2: Told him to go ahead
pid=2: Got 2 responses and 2 pids to notify
pid=3: New message in inbox from 0, its a response
pid=3: Got 1 responses and 3 pids to notify
pid=3: New message in inbox from 1, its a response
pid=3: Got 2 responses and 3 pids to notify
pid=3: New message in inbox from 2, its a response
pid=3: Got 3 responses and 3 pids to notify
pid=3: Got all responses
pid=3: database at local_logical_time=12
pid:00 logclk:0006 c:1
pid:01 logclk:0006 c:1
pid:02 logclk:0006 c:1
pid:03 logclk:0012 c:2
pid=3: Done with critical code. Gonna notify 3 processes now
pid=3: Notified everybody.
pid=3: Gonna sleep now.
pid=1: New message in inbox from 3, its a response
pid=1: Got 2 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a response
pid=0: Got 1 responses and 0 pids to notify
pid=2: New message in inbox from 3, its a response
pid=2: Got 3 responses and 2 pids to notify
pid=2: Got all responses
pid=2: database at local_logical_time=12
pid:00 logclk:0006 c:1
pid:01 logclk:0006 c:1
pid:02 logclk:0012 c:2
pid:03 logclk:0012 c:2
pid=2: Done with critical code. Gonna notify 2 processes now
pid=2: Notified everybody.
pid=2: Gonna sleep now.
pid=1: New message in inbox from 2, its a response
pid=1: Got 3 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a response
pid=0: Got 2 responses and 0 pids to notify
pid=1: Got all responses
pid=1: database at local_logical_time=12
pid:00 logclk:0006 c:1
pid:01 logclk:0012 c:2
pid:02 logclk:0012 c:2
pid:03 logclk:0012 c:2
pid=1: Done with critical code. Gonna notify 1 processes now
pid=1: Notified everybody.
pid=1: Gonna sleep now.
pid=0: New message in inbox from 1, its a response
pid=0: Got 3 responses and 0 pids to notify
pid=0: Got all responses
pid=0: database at local_logical_time=12
pid:00 logclk:0012 c:2
pid:01 logclk:0012 c:2
pid:02 logclk:0012 c:2
pid:03 logclk:0012 c:2
pid=0: Done with critical code. Gonna notify 0 processes now
pid=0: Notified everybody.
pid=0: Gonna sleep now.
pid=2: I want to use the database
pid=2: Waiting for responses
pid=3: I want to use the database
pid=3: Waiting for responses
pid=3: New message in inbox from 2, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 1 pids to notify
pid=2: New message in inbox from 3, its a request
pid=2: Told him to go ahead
pid=2: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 2, its a response
pid=3: Got 1 responses and 1 pids to notify
pid=0: I want to use the database
pid=0: Waiting for responses
pid=0: New message in inbox from 2, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=0: New message in inbox from 3, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=2: New message in inbox from 0, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 1 pids to notify
pid=3: New message in inbox from 0, its a request
pid=3: I'll notify him later on
pid=3: Got 1 responses and 2 pids to notify
pid=2: New message in inbox from 0, its a response
pid=2: Got 1 responses and 1 pids to notify
pid=3: New message in inbox from 0, its a response
pid=3: Got 2 responses and 2 pids to notify
pid=1: I want to use the database
pid=1: Waiting for responses
pid=1: New message in inbox from 0, its a request
pid=1: I'll notify him later on
pid=1: Got 0 responses and 1 pids to notify
pid=1: New message in inbox from 2, its a request
pid=1: Told him to go ahead
pid=1: Got 0 responses and 1 pids to notify
pid=1: New message in inbox from 3, its a request
pid=1: Told him to go ahead
pid=1: Got 0 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a request
pid=3: I'll notify him later on
pid=3: Got 2 responses and 3 pids to notify
pid=0: New message in inbox from 1, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=2: New message in inbox from 1, its a request
pid=2: I'll notify him later on
pid=2: Got 1 responses and 2 pids to notify
pid=1: New message in inbox from 0, its a response
pid=1: Got 1 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a response
pid=3: Got 3 responses and 3 pids to notify
pid=2: New message in inbox from 1, its a response
pid=2: Got 2 responses and 2 pids to notify
pid=3: Got all responses
pid=3: database at local_logical_time=18
pid:00 logclk:0012 c:2
pid:01 logclk:0012 c:2
pid:02 logclk:0012 c:2
pid:03 logclk:0018 c:3
pid=3: Done with critical code. Gonna notify 3 processes now
pid=3: Notified everybody.
pid=3: Gonna sleep now.
pid=0: New message in inbox from 3, its a response
pid=0: Got 1 responses and 0 pids to notify
pid=2: New message in inbox from 3, its a response
pid=2: Got 3 responses and 2 pids to notify
pid=1: New message in inbox from 3, its a response
pid=1: Got 2 responses and 1 pids to notify
pid=2: Got all responses
pid=2: database at local_logical_time=18
pid:00 logclk:0012 c:2
pid:01 logclk:0012 c:2
pid:02 logclk:0018 c:3
pid:03 logclk:0018 c:3
pid=2: Done with critical code. Gonna notify 2 processes now
pid=2: Notified everybody.
pid=2: Gonna sleep now.
pid=1: New message in inbox from 2, its a response
pid=1: Got 3 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a response
pid=0: Got 2 responses and 0 pids to notify
pid=1: Got all responses
pid=1: database at local_logical_time=18
pid:00 logclk:0012 c:2
pid:01 logclk:0018 c:3
pid:02 logclk:0018 c:3
pid:03 logclk:0018 c:3
pid=1: Done with critical code. Gonna notify 1 processes now
pid=1: Notified everybody.
pid=1: Gonna sleep now.
pid=0: New message in inbox from 1, its a response
pid=0: Got 3 responses and 0 pids to notify
pid=0: Got all responses
pid=0: database at local_logical_time=18
pid:00 logclk:0018 c:3
pid:01 logclk:0018 c:3
pid:02 logclk:0018 c:3
pid:03 logclk:0018 c:3
pid=0: Done with critical code. Gonna notify 0 processes now
pid=0: Notified everybody.
pid=0: Gonna sleep now.
pid=0: I want to use the database
pid=0: Waiting for responses
pid=3: I want to use the database
pid=3: Waiting for responses
pid=3: New message in inbox from 0, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 0, its a response
pid=3: Got 1 responses and 1 pids to notify
pid=1: I want to use the database
pid=1: Waiting for responses
pid=1: New message in inbox from 0, its a request
pid=1: I'll notify him later on
pid=1: Got 0 responses and 1 pids to notify
pid=1: New message in inbox from 3, its a request
pid=1: Told him to go ahead
pid=1: Got 0 responses and 1 pids to notify
pid=0: New message in inbox from 1, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 1, its a request
pid=3: I'll notify him later on
pid=3: Got 1 responses and 2 pids to notify
pid=1: New message in inbox from 0, its a response
pid=1: Got 1 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a response
pid=3: Got 2 responses and 2 pids to notify
pid=2: I want to use the database
pid=2: Waiting for responses
pid=2: New message in inbox from 0, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 1 pids to notify
pid=2: New message in inbox from 1, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 2 pids to notify
pid=2: New message in inbox from 3, its a request
pid=2: Told him to go ahead
pid=2: Got 0 responses and 2 pids to notify
pid=0: New message in inbox from 2, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 2, its a request
pid=3: I'll notify him later on
pid=3: Got 2 responses and 3 pids to notify
pid=1: New message in inbox from 2, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=2: New message in inbox from 0, its a response
pid=2: Got 1 responses and 2 pids to notify
pid=2: New message in inbox from 1, its a response
pid=2: Got 2 responses and 2 pids to notify
pid=3: New message in inbox from 2, its a response
pid=3: Got 3 responses and 3 pids to notify
pid=3: Got all responses
pid=3: database at local_logical_time=24
pid:00 logclk:0018 c:3
pid:01 logclk:0018 c:3
pid:02 logclk:0018 c:3
pid:03 logclk:0024 c:4
pid=3: Done with critical code. Gonna notify 3 processes now
pid=3: Notified everybody.
pid=3: Gonna sleep now.
pid=1: New message in inbox from 3, its a response
pid=1: Got 2 responses and 1 pids to notify
pid=2: New message in inbox from 3, its a response
pid=2: Got 3 responses and 2 pids to notify
pid=0: New message in inbox from 3, its a response
pid=0: Got 1 responses and 0 pids to notify
pid=2: Got all responses
pid=2: database at local_logical_time=24
pid:00 logclk:0018 c:3
pid:01 logclk:0018 c:3
pid:02 logclk:0024 c:4
pid:03 logclk:0024 c:4
pid=2: Done with critical code. Gonna notify 2 processes now
pid=2: Notified everybody.
pid=2: Gonna sleep now.
pid=0: New message in inbox from 2, its a response
pid=0: Got 2 responses and 0 pids to notify
pid=1: New message in inbox from 2, its a response
pid=1: Got 3 responses and 1 pids to notify
pid=1: Got all responses
pid=1: database at local_logical_time=24
pid:00 logclk:0018 c:3
pid:01 logclk:0024 c:4
pid:02 logclk:0024 c:4
pid:03 logclk:0024 c:4
pid=1: Done with critical code. Gonna notify 1 processes now
pid=1: Notified everybody.
pid=1: Gonna sleep now.
pid=0: New message in inbox from 1, its a response
pid=0: Got 3 responses and 0 pids to notify
pid=0: Got all responses
pid=0: database at local_logical_time=24
pid:00 logclk:0024 c:4
pid:01 logclk:0024 c:4
pid:02 logclk:0024 c:4
pid:03 logclk:0024 c:4
pid=0: Done with critical code. Gonna notify 0 processes now
pid=0: Notified everybody.
pid=0: Gonna sleep now.
pid=1: I want to use the database
pid=1: Waiting for responses
pid=0: I want to use the database
pid=0: Waiting for responses
pid=0: New message in inbox from 1, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=1: New message in inbox from 0, its a request
pid=1: I'll notify him later on
pid=1: Got 0 responses and 1 pids to notify
pid=1: New message in inbox from 0, its a response
pid=1: Got 1 responses and 1 pids to notify
pid=3: I want to use the database
pid=3: Waiting for responses
pid=3: New message in inbox from 0, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 1 pids to notify
pid=3: New message in inbox from 1, its a request
pid=3: I'll notify him later on
pid=3: Got 0 responses and 2 pids to notify
pid=1: New message in inbox from 3, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=3: New message in inbox from 0, its a response
pid=3: Got 1 responses and 2 pids to notify
pid=3: New message in inbox from 1, its a response
pid=3: Got 2 responses and 2 pids to notify
pid=2: I want to use the database
pid=2: Waiting for responses
pid=2: New message in inbox from 0, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 1 pids to notify
pid=2: New message in inbox from 1, its a request
pid=2: I'll notify him later on
pid=2: Got 0 responses and 2 pids to notify
pid=2: New message in inbox from 3, its a request
pid=2: Told him to go ahead
pid=2: Got 0 responses and 2 pids to notify
pid=3: New message in inbox from 2, its a request
pid=3: I'll notify him later on
pid=3: Got 2 responses and 3 pids to notify
pid=1: New message in inbox from 2, its a request
pid=1: Told him to go ahead
pid=1: Got 1 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a request
pid=0: Told him to go ahead
pid=0: Got 0 responses and 0 pids to notify
pid=2: New message in inbox from 0, its a response
pid=2: Got 1 responses and 2 pids to notify
pid=2: New message in inbox from 1, its a response
pid=2: Got 2 responses and 2 pids to notify
pid=3: New message in inbox from 2, its a response
pid=3: Got 3 responses and 3 pids to notify
pid=3: Got all responses
pid=3: database at local_logical_time=30
pid:00 logclk:0024 c:4
pid:01 logclk:0024 c:4
pid:02 logclk:0024 c:4
pid:03 logclk:0030 c:5
pid=3: Done with critical code. Gonna notify 3 processes now
pid=3: Notified everybody.
pid=3: No more critical code for me.
pid=1: New message in inbox from 3, its a response
pid=1: Got 2 responses and 1 pids to notify
pid=0: New message in inbox from 3, its a response
pid=0: Got 1 responses and 0 pids to notify
pid=2: New message in inbox from 3, its a response
pid=2: Got 3 responses and 2 pids to notify
pid=2: Got all responses
pid=2: database at local_logical_time=30
pid:00 logclk:0024 c:4
pid:01 logclk:0024 c:4
pid:02 logclk:0030 c:5
pid:03 logclk:0030 c:5
pid=2: Done with critical code. Gonna notify 2 processes now
pid=2: Notified everybody.
pid=2: No more critical code for me.
pid=1: New message in inbox from 2, its a response
pid=1: Got 3 responses and 1 pids to notify
pid=0: New message in inbox from 2, its a response
pid=0: Got 2 responses and 0 pids to notify
pid=1: Got all responses
pid=1: database at local_logical_time=30
pid:00 logclk:0024 c:4
pid:01 logclk:0030 c:5
pid:02 logclk:0030 c:5
pid:03 logclk:0030 c:5
pid=1: Done with critical code. Gonna notify 1 processes now
pid=1: Notified everybody.
pid=1: No more critical code for me.
pid=0: New message in inbox from 1, its a response
pid=0: Got 3 responses and 0 pids to notify
pid=0: Got all responses
pid=0: database at local_logical_time=30
pid:00 logclk:0030 c:5
pid:01 logclk:0030 c:5
pid:02 logclk:0030 c:5
pid:03 logclk:0030 c:5
pid=0: Done with critical code. Gonna notify 0 processes now
pid=0: Notified everybody.
pid=0: No more critical code for me.
pid=3: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 30
pid=2: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 30
pid=1: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 30
pid=0: Got no messages for 20 seconds, gonna quit with status code 0. Final local time: 30
```

</details>

## Lab 2

Zadatak: Ostvariti programski sustav za izradu digitalne omotnice, digitalnog potpisa te digitalnog pečata koristeći već gotove, slobodno dostupne algoritme. Od kriptografskih algoritama treba korisniku omogućiti izbor svih navedenih algoritama iz svake kategorije:

- Simetrični kriptosustav: AES i 3-DES. Ponuditi na izbor sve moguće veličine ključeva za svaki algoritam te najmanje dva načina kriptiranja (ECB, CBC, OFB, CFB, CTR, ...).
- Asimetrični kriptosustav: RSA, ponuditi nekoliko različitih veličina ključeva.
- Funkcija za izračunavanje sažetka poruke (hash funkcija): SHA-2 ili SHA-3. Omogućiti izbor između najmanje dvije od četiri inačice algoritma, npr. SHA3-256 i SHA3-512).

Nije obavezno, ali je poželjno (zbog dodatnih bodova) ostvariti proizvoljno grafičko sučelje.

Prilikom pokretanja programa inicijalno moraju biti podešene vrijedosti svih elemenata sučelja (imena datoteka, duljine ključeva, ...) i odgovarajuće ulazne datoteke moraju postojati (npr. u direktoriju gdje se nalazi program) tako da se program može ODMAH pokrenuti sa zadanim parametrima.

Preporučeni [formati datoteka](http://www.zemris.fer.hr/predmeti/os2/kriptografija/kljucevi.html).

✓

Za pokrenuti testove: `./test.py`

Za pokrenuti demo: `./demo.sh`

<details>
  <summary>Ispis nakon pokretanja `./demo.py`:</summary>

```js
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  KEY GENERATION  ~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~ #
Namespace(action_command='gen', n=3072, savedir='keys', private_key_filename='id_rsa', public_key_filename='id_rsa.pub')
Path to private key: keys/id_rsa
Path to public key: keys/id_rsa.pub
✓
# ~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  ENVELOPE  ~~~~ #
# ~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  AES192 + OFB  ~~~~ #
# ~~~~  CREATE ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='create', sym_algo='AES', sym_key='12345678abcdefgh87654321', sym_key_length=24, sym_iv='12345678abcdefgh', sym_mode='OFB', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Message loaded
Public key loaded
Envelope (sym_enc_msg, pub_enc_secret)
Envelope part1 (sym_enc_msg) path: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path: envelope/envelope.part2
✓
# ~~~~  OPEN ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='open', sym_algo='AES', sym_key=None, sym_key_length=24, sym_iv=None, sym_mode='OFB', private_key_path='keys/id_rsa', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Private key loaded
Envelope part1 (sym_enc_msg) path given as: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path given as: envelope/envelope.part2
Envelope loaded
Sym Key ('b'): b'12345678abcdefgh87654321'
Sym Key (utf-8): 12345678abcdefgh87654321
Sym IV ('b'): b'12345678abcdefgh'
Sym IV (utf-8): 12345678abcdefgh
Message ('b'): b'jure i mate\n'
Message (utf8): jure i mate

✓
# ~~~~  AES256 + CFB  ~~~~ #
# ~~~~  CREATE ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='create', sym_algo='AES', sym_key='12345678abcdefgh87654321hgfedcba', sym_key_length=24, sym_iv='12345678abcdefgh', sym_mode='CFB', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Message loaded
Public key loaded
Envelope (sym_enc_msg, pub_enc_secret)
Envelope part1 (sym_enc_msg) path: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path: envelope/envelope.part2
✓
# ~~~~  OPEN ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='open', sym_algo='AES', sym_key=None, sym_key_length=32, sym_iv=None, sym_mode='CFB', private_key_path='keys/id_rsa', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Private key loaded
Envelope part1 (sym_enc_msg) path given as: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path given as: envelope/envelope.part2
Envelope loaded
Sym Key ('b'): b'12345678abcdefgh87654321hgfedcba'
Sym Key (utf-8): 12345678abcdefgh87654321hgfedcba
Sym IV ('b'): b'12345678abcdefgh'
Sym IV (utf-8): 12345678abcdefgh
Message ('b'): b'jure i mate\n'
Message (utf8): jure i mate

✓
# ~~~~  3DES + ECB  ~~~~ #
# ~~~~  CREATE ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='create', sym_algo='3DES', sym_key='12345678abcdefgh87654321', sym_key_length=24, sym_iv=None, sym_mode='ECB', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Message loaded
Public key loaded
Envelope (sym_enc_msg, pub_enc_secret)
Envelope part1 (sym_enc_msg) path: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path: envelope/envelope.part2
✓
# ~~~~  OPEN ENVELOPE  ~~~~ #
Namespace(action_command='envelope', envelope_action='open', sym_algo='3DES', sym_key=None, sym_key_length=24, sym_iv=None, sym_mode='ECB', private_key_path='keys/id_rsa', envelope_savedir='envelope', envelope_part1_filename='envelope.part1', envelope_part2_filename='envelope.part2')
Private key loaded
Envelope part1 (sym_enc_msg) path given as: envelope/envelope.part1
Envelope part2 (pub_enc_secret) path given as: envelope/envelope.part2
Envelope loaded
Sym Key ('b'): b'12345678abcdefgh87654321'
Sym Key (utf-8): 12345678abcdefgh87654321
Sym IV ('b'): b''
Sym IV (utf-8): 
Message ('b'): b'jure i mate\n'
Message (utf8): jure i mate

✓
# ~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  SIGNATURE  ~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  hash_fn  ~~~~ #
# ~~~~  SIGN MESSAGE  ~~~~ #
Namespace(action_command='signature', signature_action='sign', hash_fn_name='MD5', message_path='messages/alice.txt', private_key_path='keys/id_rsa', signature_path='signatures/alice.sign')
Message loaded
Private key loaded
Signed saved: signatures/alice.sign
✓
# ~~~~  VERIFY VALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='MD5', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature OK
✓
# ~~~~  VERIFY INVALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='MD5', message_path='messages/alice_modified.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature INVALID
✓
# ~~~~  hash_fn  ~~~~ #
mkdir: cannot create directory ‘signatures’: File exists
# ~~~~  SIGN MESSAGE  ~~~~ #
Namespace(action_command='signature', signature_action='sign', hash_fn_name='SHA256', message_path='messages/alice.txt', private_key_path='keys/id_rsa', signature_path='signatures/alice.sign')
Message loaded
Private key loaded
Signed saved: signatures/alice.sign
✓
# ~~~~  VERIFY VALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA256', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature OK
✓
# ~~~~  VERIFY INVALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA256', message_path='messages/alice_modified.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature INVALID
✓
# ~~~~  hash_fn  ~~~~ #
mkdir: cannot create directory ‘signatures’: File exists
# ~~~~  SIGN MESSAGE  ~~~~ #
Namespace(action_command='signature', signature_action='sign', hash_fn_name='SHA3_512', message_path='messages/alice.txt', private_key_path='keys/id_rsa', signature_path='signatures/alice.sign')
Message loaded
Private key loaded
Signed saved: signatures/alice.sign
✓
# ~~~~  VERIFY VALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA3_512', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature OK
✓
# ~~~~  VERIFY INVALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA3_512', message_path='messages/alice_modified.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature INVALID
✓
# ~~~~  hash_fn  ~~~~ #
mkdir: cannot create directory ‘signatures’: File exists
# ~~~~  SIGN MESSAGE  ~~~~ #
Namespace(action_command='signature', signature_action='sign', hash_fn_name='SHA384', message_path='messages/alice.txt', private_key_path='keys/id_rsa', signature_path='signatures/alice.sign')
Message loaded
Private key loaded
Signed saved: signatures/alice.sign
✓
# ~~~~  VERIFY VALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA384', message_path='messages/alice.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature OK
✓
# ~~~~  VERIFY INVALID SIGNATURE  ~~~~ #
Namespace(action_command='signature', signature_action='verify', hash_fn_name='SHA384', message_path='messages/alice_modified.txt', public_key_path='keys/id_rsa.pub', signature_path='signatures/alice.sign')
Message loaded
Public key loaded
Signed hash loaded
Signature INVALID
✓
# ~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  CERTIFICATE  ~~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~~  ALICE GENERATES HER KEYS -- RSA 2048  ~~~~ #
Namespace(action_command='gen', n=2048, savedir='keys/alice', private_key_filename='id_rsa', public_key_filename='id_rsa.pub')
Path to private key: keys/alice/id_rsa
Path to public key: keys/alice/id_rsa.pub
✓
# ~~~~  BOB GENERATES HIS KEYS -- RSA 3072  ~~~~ #
Namespace(action_command='gen', n=3072, savedir='keys/bob', private_key_filename='id_rsa', public_key_filename='id_rsa.pub')
Path to private key: keys/bob/id_rsa
Path to public key: keys/bob/id_rsa.pub
✓

# ~~~~  ALICE CREATES A CERTIFICATE  ~~~~ #
Namespace(action_command='cert', certificate_action='create', hash_fn_name='SHA3_512', message_path='messages/alice.txt', private_key_path='keys/alice/id_rsa', public_key_path='keys/bob/id_rsa.pub', sym_algo='AES', sym_key='12345678abcdefgh87654321', sym_key_length=24, sym_iv='12345678abcdefgh', sym_mode='OFB', cert_savedir='certificates/alice', cert_part1_filename='cert.part1', cert_part2_filename='cert.part2', cert_part3_filename='cert.part3')
Message loaded
Public key loaded
Private key loaded
Certificate (sym_enc_msg, pub_enc_secret, signed_hash)
Certificate part1 (sym_enc_msg) path: certificates/alice/cert.part1
Certificate part2 (pub_enc_secret) path: certificates/alice/cert.part2
Certificate part3 (signed_hash) path: certificates/alice/cert.part3
✓
# ~~~~  BOB OPENS THE CERTIFICATE -- BUT FORGETS WHICH KEY WAS WHICH AND SWITCHES THEM  ~~~~ #
Namespace(action_command='cert', certificate_action='open', hash_fn_name='SHA3_512', private_key_path='keys/alice/id_rsa.pub', public_key_path='keys/bob/id_rsa', sym_algo='AES', sym_key=None, sym_key_length=24, sym_iv=None, sym_mode='OFB', cert_savedir='certificates/alice', cert_part1_filename='cert.part1', cert_part2_filename='cert.part2', cert_part3_filename='cert.part3')
Public key loaded
Private key loaded
Certificate (sym_enc_msg, pub_enc_secret, signed_hash)
Certificate part1 (sym_enc_msg) path given as: certificates/alice/cert.part1
Certificate part2 (pub_enc_secret) path given as: certificates/alice/cert.part2
Certificate part3 (signed_hash) path given as: certificates/alice/cert.part3
Certificate loaded.
Signature INVALID
✓
# ~~~~  BOB OPENS THE CERTIFICATE -- WITH CORRECT KEYS  ~~~~ #
Namespace(action_command='cert', certificate_action='open', hash_fn_name='SHA3_512', private_key_path='keys/bob/id_rsa', public_key_path='keys/alice/id_rsa.pub', sym_algo='AES', sym_key=None, sym_key_length=24, sym_iv=None, sym_mode='OFB', cert_savedir='certificates/alice', cert_part1_filename='cert.part1', cert_part2_filename='cert.part2', cert_part3_filename='cert.part3')
Public key loaded
Private key loaded
Certificate (sym_enc_msg, pub_enc_secret, signed_hash)
Certificate part1 (sym_enc_msg) path given as: certificates/alice/cert.part1
Certificate part2 (pub_enc_secret) path given as: certificates/alice/cert.part2
Certificate part3 (signed_hash) path given as: certificates/alice/cert.part3
Certificate loaded.
Singature OK
Sym key ('b'): b'12345678abcdefgh87654321'
Sym key (utf-8): 12345678abcdefgh87654321
Sym IV ('b'): b'12345678abcdefgh'
Sym IV (utf-8): 12345678abcdefgh
Message ('b'): b'jure i mate\n'
Message (utf8): jure i mate

✓
# ~~~~  BOB OPENS THE CERTIFICATE -- BUT EVE TRIED TO CHANGE the encrypted message sym_enc_msg (cert.part1)  ~~~~ #
Namespace(action_command='cert', certificate_action='open', hash_fn_name='SHA3_512', private_key_path='keys/bob/id_rsa', public_key_path='keys/alice/id_rsa.pub', sym_algo='AES', sym_key=None, sym_key_length=24, sym_iv=None, sym_mode='OFB', cert_savedir='certificates/alice', cert_part1_filename='cert.part1.eve', cert_part2_filename='cert.part2', cert_part3_filename='cert.part3')
Public key loaded
Private key loaded
Certificate (sym_enc_msg, pub_enc_secret, signed_hash)
Certificate part1 (sym_enc_msg) path given as: certificates/alice/cert.part1.eve
Certificate part2 (pub_enc_secret) path given as: certificates/alice/cert.part2
Certificate part3 (signed_hash) path given as: certificates/alice/cert.part3
Certificate loaded.
Signature INVALID
✓
```

<details>