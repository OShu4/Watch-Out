 ![alt text](https://github.com/OShu4/Watch-Out/blob/main/Watch-Out/src/main/python/assets/Logo/applogo.png) 
# Watch-Out!
## Introduzione al progetto

### Scopo del programma: 
##### Creazione di un reaction-game strutturato in 5 livelli. Il giocatore affronterà quindi 5 diversi nemici, con stage a difficoltà crescente, con sempre meno tempo per agire, in un ambiente retrò coinvolgente.

## Sviluppato con 
- Python, libreria pygame

## Partecipanti del gruppo
- **Galantini Corrado**
- **Gallo Valerio**
- **Aprea Mario**      
- **Di Muzio Pietro**
- **Pesaresi Adriano** 
- **Sturniolo Edoardo**

### Installazione del videogioco
L'applicativo sarà scaricabile mediante l'apposito bottone *download* nel sito ufficiale del gioco "link".

## WatchOut.exe e download

### Spiegazione generale del funzionamento del menu del videogioco:
Il gioco, una volta installato e avviato, presenterà un menu di scelta dove l'utente potrà decidere tra:
* **Play** -> Avvia il gioco, partendo dal primo livello.

* **Set Easy** -> Semplifica il livello di gioco, rallentando i timer prima dello scatto del Watch-Out!
* **Select level** -> Una volta completato il gioco almeno una volta, il giocatore sarà abilitato alla scelta di uno dei 5 livelli disponibili da giocare.
* **Quit** -> Chiude il processo del gioco.


Una volta avviata la partita l'utente troverà a schermo una mappa occupata da due personaggi *(da ora **pg**)*, il pg del giocatore e quello avversario, governato dal computer. I pg rimarranno fermi durante tutto il corso della partita. Dopo un intervallo randomico di secondi apparirà a schermo la scritta **Watch Out**, a quel punto il giocatore dovrà premere il tasto sinistro del mouse prima del pg nemico, aggiudicandosi la vittoria ed il lascia passare al livello successivo.
Inoltre il giocatore, sempre nella schermata di gioco, in alto a destra, troverà il suo numero di vite rimanenti. A partire da 5. Ogni volta che perderà verranno diminuite di 1. Una volta terminate, sarà game over e dovrà ricominciare il gioco da capo.
   

## Classi
### - [-] main.py  
classe gestisce le interazioni di gioco. Le funzioni principali presenti nella classe sono:
-**play()** che viene richiamata al click del pulsante Play nel menu. Compone la struttura principale di gioco.
```python
 while True:
      clock.tick(FPS)
      key_input = pygame.key.get_pressed()
      MENU_MOUSE_POS = pygame.mouse.get_pos()
```
While che si ripete 120 volte (FPS) e controlla eventuali eventi:
-key_input -> eventuali click sulla tastiera.
-MENU_MOUSE_POS -> posizione del mouse
-event in pygame.event.get() -> eventi del mouse

```python
 if ENEMY_NUMBER == "5":
     isMENU = True
     Return=False
     if not EASY_DIFF:
         fin = ' '.join(format(ord(x), 'b') for x in "completed")
         FileManager.writeTO(fin, "fin")
     draw_winner("GAME OVER!", False, G)
 if PG_HP == 0:
     isMENU = True
     draw_winner("GAME OVER!", False, R)
```
Verifica della vittoria (*ENEMY_NUMBER == "5"*), con conseguente creazione del file fin.bin nel caso di gioco completato in normal.
Verifica di sconfitta (*PG_HP == "0"*), con uscita dalla scermata play e reindirizzamento al menu.

-**set_level()** richiamata al click del pulsante Select Level nel menu. Permette, se e solo se il gioco e' gia precedentemente stato completato in modalita normale, di scegliere un livello da rigiocare.

-**main_menu()** richiamata all'avvio del gioco, permette di scegliere cosa fare nel gioco:
-PLAY
-SET EASY -> cambia la difficolta del gioco.
-SELECT LEVEL
-QUIT

### - [-] button.py 
Utilizzata da tutti i bottoni del gioco. 
```python
 def __init__(self, image, pos, text_input, font, base_color, hovering_color, overImage):
        self.image = image
        self.imageSupp=image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.isOvered=False
        self.overImage=overImage
```
Costruttore di Button che, tra i parametri principali, riceve:
-**image** -> l'immagine di sfondo del bottone
-**pos** -> la posizione nella finestra del bottone
-**text_input** -> testo sul bottone
-**base_color** -> colore del testo mentre il bottone non e' overato
-**hovering_colot** -> colore del testo mentre il bottone e' overato
-**verImage** -> resize del immagine mentre il bottobe e' overato

### - [-] fileManager.py
file che gestisce la creazione, la scrittura e la lettura da file.
```python
    def writeTO(time, file):
        path="Watch-Out/src/main/python/data/"+file+".bin"
        f = open(path, "wb")
        if isfloat(time):
            byteResult = FileManager.float_to_bin(time)
            f.write(bytearray(byteResult, "utf8"))
        else:
            f.write(bytearray(time, "utf8"))
        return
```
Scrittura su *file*. Separa la possibilita in cui il testo in input sia float o string

```python
    def getToFile(file):
        path="Watch-Out/src/main/python/data/"+file+".bin"
        if not exists(path):
            return "non esiste"
        file = open(path, "rb")
        byte = file.read(1)
        byteScore = bytes()
        while byte:
            byteScore = byteScore + byte
            byte = file.read(1)
        return byteScore
```
Legge da file binari.

```python
    def JsonReader(path):
        with open(path) as f:
            data = json.load(f)

        w = data["frames"]["images"] ["frame"] ["w"] 
        h = data["frames"]["images"] ["frame"] ["h"] 
        size =[w,h] 
        return size
```
Legge da file Json altezza e spessore degli sprite

### - [-] spritesheet.py
Crea un oggetto di tipo spritesheet.
```python
	def get_image(self, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.fill(colour)
    image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    return image
```
Gestisce i frame degli sprite.
## Ulteriori informazioni

### Sprite & Assets
Gli sprite, o pixel-art del gioco sono stati disegnati attraverso il software Piskel, a mano. Ogni singolo disegno è originale, inoltre i disegni sono animati a 2 frame per secondo all'interno del gioco.

### Traguardi
- [❌] Funzionamento del gioco su MacOS.
- [✔️] Gestione variabili d'ambiente.
- [✔️] Ottimizzazione per diminuzione dell'uso in percentuale della CPU.
- [✔️] Salvataggio dei dati in file binari. (Dati del punteggio del giocatore, e dati del completamento dei livelli.)
- [✔️] Creazione di tutte le pixel-art.
- [✔️] Sistema delle vite.

## Sito Web
- Collegamento: https://watch-out2022.000webhostapp.com/
- Sviluppato con HTML, CSS, raccolta di strumenti BOOTSTRAP 5.
- 
## Licenza
MIT License

Copyright (c) 2022 Corrado Galantini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contatti

### Galantini Corrado
- galantini.corrado@istitutomontani.edu.it
- Git <a href="https://github.com/OShu4">OShu4 </a> 
- Discord Mario Giordano#3698

### Gallo Valerio
- gallo.valerio@istitutomontani.edu.it
- Git <a href="https://github.com/Vallozz">Vallozz </a>

### Adriano Pesaresi
- pesaresi.adriano@istitutomontani.edu.it
- Git <a href="https://github.com/adrianopesaresi">adrianopesaresi </a>
