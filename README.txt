Marcu-Nicolescu Cezar-George
335CB

Voi descrie tema in functie de clasa si de operatiile facute in interiorul acesteia.

Pentru clasa Producer :

	Merg prin lista de produse , luand produs cu produs. Apoi sparg produsul curent in prod (id1 de exemplu) , cantitate produsa si timpul de productie. Calculez timpul total de productie inmultind cantitatea cu timpul de productie al unui obiect/produs si astept pana cand acesta este realizat.
Apoi incep publicarea pe marketplace a cate unui obiect pana cand ajung la cantitatea dorita de a fi adaugata in piata/magazin (marketplace).
Daca aceasta actiune nu s-a realizat (metoda publish mi-a intors false) inseamna ca queue-ul meu este plin si ar trebui sa astept pana se mai elibereaza. Fac producatorul sa astept timpul specificat de asteptare pentru aceasta situatie (republish_wait_time) si , cat timp incercarile producatorului de a publica nu au succes ar trebui sa astepte.


Pentru clasa Consumer:

	Privim carts ca o lista de carucioare, iar un carucior ca o lista
de cumparaturi , in sensul ca poti adauga sau scoate in cazul in care
te razgandezi.  Comenzi reprezinta un element de pe lista de cumparaturi. Sparg in functie de tipul actiunii (daca isi doreste sa adauge sau sa scoata), de cantitate (cate produse vrea sa elimine/ adauge in cos) si pe ce produs se efectueaza prelucrarea.
Daca actiunea este aceea de adaugare , introduc in caruciorul curent produsul dorit (cel cu id-ul dat ca parametru metodei add_to_cart), actiunea repetandu-se de un numar de ori egal cu cantintatea.
Daca metoda imi intoarce false inseamna ca produsul nu este pe stoc , deci clientul trebuie sa astepte pana cand devine disponibil produsul.
Intr-un loop while fac clientul sa astepte un timp dat ca parametru pana cand reuseste sa ia acel produs.
	Cazul in care am remove din carucior (type-ul comenzii este remove ) consta in apelarea functiei de remove_from_cart pana cand cantitatea ce se doreste a fi eliminata este respectata.
      La final , returnez caruciorul de cumparaturi, o lista de produse, si incep afisarea acestora.


Pentru clasa Marketplace:
	
    In fiecare metoda ce imi face efectiv prelucrare/ verificare
de date am folosit un mutex pentru a face metoda thread safe.
    In metoda publish am verificat sa lista producatorului sa nu depaseasca dimensiunea maxima admisa (queue size) , daca corespunde acestei cerinte , am adaugat produsul in lista si am returnat ca am reusit (true) . Daca nu e spatiu , intorc false.

    In metoda add_to_cart merg prin lista de producatori , verificand fiecare produs al acestora pana cand gasesc unul ce corespunde cu cel primit ca parametru . Odata gasit , il adaug in cos , retin de unde l-am cumparat(producatorul), produsul cumparat si in ce carucior l-am adaugat intr-o lista pe care o verific in caz ca un client doreste sa restituie produsul, iar apoi ies din functie.

   In metoda remove_from_cart caut in cosul cu id-ul primit ca parametru produsul ce trebuie scos , il scot , iar apoi il restitui producatorului cu ajutorul listei "restituireLaProd" in care retin toate detaliile necesare anexarii dinou la lista producatorului


