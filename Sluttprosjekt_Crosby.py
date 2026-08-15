#Importerer nødvendige biblioteker
import random as rd
import pygame as pg
import time
from pygame.locals import (K_UP, K_DOWN, K_LEFT, K_RIGHT)
import sys

#Definerer nødvendige farger
BLÅ = (50, 50, 165)
GRØNN = (100, 200, 100)
LYS_GRØNN = (70, 255, 70)
RØD = (200, 100, 100)
GULL = (230, 190, 70)
SVART = (0,0,0)

#Importerer fil for highscore
HIGHSCORE_FIL = "Sluttprosjekt_Crosby_highscore.txt"


#Klasse for å lage en slange som kan flyttes på og vokse
class Slange:
  def __init__(self, koordinater):
    self.koordinater = koordinater
    self.mett = False
    self.kollisjon = False

  def flytt_opp(self):
    punkt = (self.koordinater[0][0], self.koordinater[0][1] - 1)
    self.koordinater.insert(0,punkt)
    if self.mett:
      self.mett = False
    else:
      self.koordinater.pop()

  def flytt_ned(self):
    punkt = (self.koordinater[0][0], self.koordinater[0][1] + 1)
    self.koordinater.insert(0,punkt)
    if self.mett:
      self.mett = False
    else:
      self.koordinater.pop()

  def flytt_venstre(self):
    punkt = (self.koordinater[0][0] - 1, self.koordinater[0][1])
    self.koordinater.insert(0,punkt)
    if self.mett:
      self.mett = False
    else:
      self.koordinater.pop()

  def flytt_høyre(self):
    punkt = (self.koordinater[0][0] + 1, self.koordinater[0][1])
    self.koordinater.insert(0,punkt)
    if self.mett:
      self.mett = False
    else:
      self.koordinater.pop()

  def tegn(self):    
    for koordinat in self.koordinater:
      pg.draw.rect(vindu, BLÅ, ((koordinat[0]) * CELLESTØRRELSE, (koordinat[1]) * CELLESTØRRELSE, CELLESTØRRELSE, CELLESTØRRELSE))
  
  def hent_hode(self):
    return self.koordinater[0]
  
  def spis_eple(self):
    self.mett = True
  
  def sjekk_kollisjon(self):
    slangehode = slangen.hent_hode()
    if slangehode[0] < 0 or slangehode[0] >= KOLONNER or slangehode[1] < 0 or slangehode[1] >= RADER:
      self.kollisjon = True
    lengde_slange = len(self.koordinater)
    if lengde_slange > 1:
      for i in range(1, lengde_slange-1): 
        if (slangehode == self.koordinater[i]):
          self.kollisjon = True

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der innholdet skal "tegnes" 
VINDU_BREDDE = 500
VINDU_HOYDE  = 500
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])

KOLONNER = 15
RADER = KOLONNER
CELLESTØRRELSE = VINDU_BREDDE // KOLONNER
FONT_SCORE = pg.font.SysFont("Arial", 24)
FONT_SLUTTSCORE = pg.font.SysFont("Arial", 35)

class Eple:
  #Klasse for å representere et eple
  def __init__(self):
    pass
  
  def plasser_eple(self):
    #Metode for å plassere eplet
    rad_eple = rd.randint(0, RADER-1)
    kolonne_eple = rd.randint(0, KOLONNER-1)
    koordinater_eple = (rad_eple, kolonne_eple)
    return(koordinater_eple)

class Rødt_eple(Eple):
  #Klasse for å representere et rødt eple som gir et poeng til brukeren om det blir spist
  def __init__(self):
    super().__init__()
  
  def tegn_eple(self, koordinater_eple):
    posisjon_eple = (koordinater_eple[0]+1)*CELLESTØRRELSE - CELLESTØRRELSE/2, (koordinater_eple[1]+1)*CELLESTØRRELSE - CELLESTØRRELSE/2
    pg.draw.circle(vindu, RØD, (posisjon_eple), CELLESTØRRELSE/2)
  
  def øk_score(self):
    return 1

class Gull_eple(Eple):
  #Klasse for å representere et gulleple som gir to poeng til brukeren om det blir spist
  def __init__(self):
    super().__init__()
  
  def tegn_eple(self, koordinater_eple):
    posisjon_eple = (koordinater_eple[0]+1)*CELLESTØRRELSE - CELLESTØRRELSE/2, (koordinater_eple[1]+1)*CELLESTØRRELSE - CELLESTØRRELSE/2
    pg.draw.circle(vindu, GULL, (posisjon_eple), CELLESTØRRELSE/2)
  
  def øk_score(self):
    return 2

eple = Rødt_eple()
koordinater_eple = eple.plasser_eple()


# Lager en todimensjonal liste som representerer brettet
brett = [[GRØNN for k in range(KOLONNER)] for r in range(RADER)]

print(type(vindu))

# Funksjon for å tegne opp brettet
def tegn_brett():
  for rad in range(RADER):
    for kol in range(KOLONNER):
      pg.draw.rect(vindu, brett[rad][kol], (kol * CELLESTØRRELSE, rad * CELLESTØRRELSE, CELLESTØRRELSE, CELLESTØRRELSE))
      pg.draw.rect(vindu, LYS_GRØNN, (kol * CELLESTØRRELSE, rad * CELLESTØRRELSE, CELLESTØRRELSE, CELLESTØRRELSE), 1)


score = "ikke påbegynt"
spill = True
while spill:
  startskjerm = True
  while startskjerm:
    vindu.fill((GRØNN))
    #Sjekker om det er en score og skriver isåfall tekst avhengig av om spilleren har spilt før eller ikke
    if score == "ikke påbegynt":
        infotekst = FONT_SLUTTSCORE.render(f"Trykk space for å starte !", True, (SVART))
        vindu.blit(infotekst, (1, VINDU_HOYDE/2))
  
    else: 
      infotekst = FONT_SLUTTSCORE.render(f"Trykk space for å starte spillet på nytt!", True, (SVART))
      vindu.blit(infotekst, (1, VINDU_HOYDE/2))
      sluttscore = FONT_SLUTTSCORE.render(f"Din score: {score}", True, (SVART))
      vindu.blit(sluttscore, (VINDU_BREDDE/4, VINDU_HOYDE/3))
      filnavn="Sluttprosjekt_Crosby_highscore.txt"
      with open(filnavn, encoding="utf-8") as fil:
        highscore = fil.read()
      highscore = FONT_SLUTTSCORE.render(f"Highscoren er: {highscore}", True, (SVART))
      vindu.blit(highscore, (VINDU_BREDDE/4, 2*VINDU_HOYDE/3))
    # Sjekker om brukeren har lukket vinduet
    for e in pg.event.get():
        if e.type == pg.QUIT:
          sys.exit()
        if e.type == pg.KEYDOWN:
          if e.key == pg.K_SPACE:
            score = 0
            retning = ""
            slangen = Slange([(7,7)])
            startskjerm = False
  
    pg.display.flip()

  # Gjenta helt til brukeren lukker vinduet
  fortsett = True
  while fortsett:
    tegn_brett()
    
    # Sjekker om brukeren har lukket vinduet
    for e in pg.event.get():
      if e.type == pg.QUIT:
        sys.exit()

    #Sjekker om en knapp har blitt trykket og setter isåfall retning til den knappen
      if e.type == pg.KEYDOWN:
        if e.key == pg.K_DOWN and retning != "opp":
          retning = "ned"
          break
        if e.key == pg.K_UP and retning != "ned":
          retning = "opp"
          break
        if e.key == pg.K_RIGHT and retning != "venstre":
          retning = "høyre"
          break
        if e.key == pg.K_LEFT and retning != "høyre":
          retning = "venstre"          
          break

    #Sjekker om teksten for retningen matcher med en av de angitte retningene og flytter isåfall slangen
    match retning: 
      case "venstre":
        slangen.flytt_venstre()
      case "høyre":
        slangen.flytt_høyre()
      case "opp":
        slangen.flytt_opp()
      case "ned":
        slangen.flytt_ned()

    slangehode = slangen.hent_hode()

    #sjekker om slangehodet og eplet befinner seg på samme sted og endrer isåfall scoren og lager nytt eple
    if slangehode[0] == koordinater_eple[0] and slangehode[1] == koordinater_eple[1]:
      score += eple.øk_score()
      slangen.spis_eple()
      tall = rd.randint(1,10)
      if tall == 1:
        eple = Gull_eple()
      else:
        eple = Rødt_eple()
      koordinater_eple = eple.plasser_eple()
    

    slangen.sjekk_kollisjon()

    #sjekker om slangen kolliderer med vegg eller seg selv og går isfåll tillbake til startskjermen
    if slangen.kollisjon:
      startskjerm = True
      with open(HIGHSCORE_FIL, encoding="utf-8") as fil:
        highscore = fil.read()
        highscore = int(highscore)
    
    #sjekker om scoren er høyere enn highscoren og endrer isåfall highscoren
      if score > highscore:
        with open(HIGHSCORE_FIL, "w") as fil:
          fil.write(f"{score}")
      fortsett = False

    slangen.tegn()
    score_tekst = FONT_SCORE.render(f"Score: {score}", True, (SVART))
    vindu.blit(score_tekst, (400, 20))
    
    eple.tegn_eple(koordinater_eple)

    #pauser programmet så tegningen skjer gradvis
    time.sleep(0.2)
    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()
    
# Avslutter pygame
pg.quit()

