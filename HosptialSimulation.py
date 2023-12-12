# -----------------------------------------------
# MSCI 333 - Simulations Project (Part 2)
#
# Created by: Aryan Ved and Yash Pokra
# -----------------------------------------------

import numpy as np
import random as rn


class Simulation:
  def __init__(self): # Initialization of Simulation
      # -- Processes --
      self.numberInSystem = 0
      self.numberInED = 0
      self.numberAmbulenceDiverted = 0

      self.numberInOR = 0
      self.numberInDischarge = 0
      self.numberInTelemetry = 0
      self.numberInICU = 0

      # -- Triage Urgency Levels --
      self.numberUrgentL1 = 0
      self.numberUrgentL2 = 0
      self.numberUrgentL3 = 0
      self.numberUrgentL4 = 0
      self.numberNonUrgentL5 = 0

      # -- Time --
      self.clock = 0
      self.timeArrivalWalkIn = self.GenerateInterarrivalTime()
      self.timeArrivalAmbulence = self.GenerateInterarrivalTime()
      self.timeDepartureED = float('inf')

      self.timeArrivalOR = 0
      self.timeArrivalICU = 0
      self.timeArrivalTelemetry = 0

      self.timeDepartureOR = float('inf')
      self.timeDepartureICU = float('inf')
      self.timeDepartureTelemetry = float('inf')

      # -- Performance Metrics --
      self.numberArrivals = 0
      self.numberDeparture = 0
      self.totalWait = 0.0

      self.utilizationInED = 0
      self.utilizationInOR = 0
      self.utilzationInTelemetry = 0
      self.utilizationInICU = 0
      self.utilizationInZone1 = 0.0
      self.utilizationInZone2 = 0.0
      self.utilizationInZone3 = 0.0
      self.utilizationInZone4 = 0.0

  def advanceTime(self):
      self.timeEvent = min(self.timeArrivalWalkIn, self.timeArrivalAmbulence, self.timeDepartureED)
      self.totalWait += self.numberInSystem * (self.timeEvent - self.clock)
      self.clock = self.timeEvent
      print("Since the last event: ")

      if self.timeArrivalWalkIn <= self.timeDepartureED:
        print("A Walk-In Patient Arrived into the ED")
        self.handleArrivalEventWalkIn()
      else:
        print("A Walk-In Patient Departed the ED")
        self.handleDepartureEventED()

      if self.timeArrivalAmbulence <= self.timeDepartureED:
        print("An Ambulence Patient Arrived into the ED")
        self.handleArrivalEventAmbulance()
      else:
        print("An Ambulence Patient Departs the ED")
        self.handleDepartureEventED()

  def handleArrivalEventWalkIn(self):
    randomVal = rn.random()
    if(self.numberInED < 40):
      if(randomVal <= 0): # 0% chance of a Level 1 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL1 += 1
        self.handleZone1(self.numberUrgentL1)
      elif(randomVal <= 0.1): # 10% chance of a Level 2 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL2 += 1
        self.handleZone2(self.numberUrgentL2)
      elif(randomVal <= 0.4): # 30% chance of a Level 3 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL3 += 1
        self.handleZone3(self.numberUrgentL3)
      elif(randomVal <= 0.8): # 40% chance of a Level 4 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL4 += 1
        self.handleZone4(self.numberUrgentL4, self.numberNonUrgentL5)
      else: # 20% chance of a Level 5 Non Urgent
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberNonUrgentL5 += 1
        self.handleZone4(self.numberUrgentL4, self.numberNonUrgentL5)


      self.timeArrivalWalkIn = self.clock + self.GenerateInterarrivalTime()
      self.timeArrivalAmbulence = self.clock + self.GenerateInterarrivalTime()

    else:
      self.numberAmbulenceDiverted = self.numberAmbulenceDiverted + 1

  def handleArrivalEventAmbulance(self):
    if(self.numberInED < 40):
      randomVal = rn.random()
      if(randomVal <= 0.2): # 20% chance of a Level 1 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL1 += 1
        self.handleZone1(self.numberUrgentL1)
      elif(randomVal <= 0.55): # 35% chance of a Level 2 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL2 += 1
        self.handleZone2(self.numberUrgentL2)
      elif(randomVal <= 0.85): # 30% chance of a Level 3 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL3 += 1
        self.handleZone3(self.numberUrgentL3)
      elif(randomVal <= 1.0): # 15% chance of a Level 4 Urgency
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberUrgentL4 += 1
        self.handleZone4(self.numberUrgentL4, self.numberNonUrgentL5)
      else: # 0% chance of a Level 5 Non Urgent
        self.numberInSystem += 1
        self.numberInED += 1
        self.numberArrivals += 1
        self.numberNonUrgentL5 += 1
        self.handleZone4(self.numberUrgentL4, self.numberNonUrgentL5)

    else:
      self.numberAmbulenceDiverted = self.numberAmbulenceDiverted + 1

    self.timeArrivalWalkIn = self.clock + self.GenerateInterarrivalTime()
    self.timeArrivalAmbulence = self.clock + self.GenerateInterarrivalTime()


  def handleDepartureEventED(self):
    if self.numberInSystem > 0:
        if self.numberInED > 0:
            self.numberInED -= 1
        if self.numberInSystem > 0:
            # Prioritizes urgent patients over non-urgent patients in the triage
            if self.numberUrgentL1 > 0:
                self.timeDepartureED = self.clock + self.GenerateServiceTime(level = 1)
                self.numberUrgentL1 -= 1
            elif self.numberUrgentL2 > 0:
                self.timeDepartureED = self.clock + self.GenerateServiceTime(level = 2)
                self.numberUrgentL2 -= 1
            elif self.numberUrgentL3 > 0:
                self.timeDepartureED = self.clock + self.GenerateServiceTime(level = 3)
                self.numberUrgentL3 -= 1
            elif self.numberUrgentL4 > 0:
                self.timeDepartureED = self.clock + self.GenerateServiceTime(level = 4)
                self.numberUrgentL4 -= 1
            else:
                self.numberNonUrgentL5 -= 1
                self.timeDepartureED = self.clock + self.GenerateServiceTime(level = 5)
        else:
            self.timeDepartureED = float('inf')

    self.utilizationInED = (self.numberInED/40)*100

  def handleZone1(self, numberUrgentL1):
      if self.numberUrgentL1 < 36:  # Total bed capacity is doubled
          randomValue = rn.random()
          if randomValue <= 0.25:
              self.numberInDischarge += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=2)
          elif randomValue <= 0.50:
              self.numberInOR += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=2)
              self.AdmittedToOR()
          elif randomValue <= 0.75:
              self.numberInICU += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=2)
              self.AdmittedToICU()
          else:
              self.numberInTelemetry += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=2)
              self.AdmittedToTelemetry()

      self.utilizationInZone1 = (self.numberUrgentL1/36)*100

  def handleZone2(self, numberUrgentL2):
      if self.numberUrgentL2 < 4:  # Total Bed capacity in Zone 2
          randomValue = rn.random()
          if randomValue <= 0.25:
              self.numberInDischarge += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=3)
          elif randomValue <= 0.50:
              self.numberInOR += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=3)
              self.AdmittedToOR()
          elif randomValue <= 0.75:
              self.numberInICU += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=3)
              self.AdmittedToICU()
          else:
              self.numberInTelemetry += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=3)
              self.AdmittedToTelemetry()

      self.utilizationInZone2 = (self.numberUrgentL2/4)*100

  def handleZone3(self, numberUrgentL3):
      if self.numberUrgentL3 < 6:
          randomValue = rn.random()
          if randomValue <= 0.25:
              self.numberInDischarge += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=4)
          elif randomValue <= 0.50:
              self.numberInOR += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=4)
              self.AdmittedToOR()
          elif randomValue <= 0.75:
              self.numberInICU += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=4)
              self.AdmittedToICU()
          else:
              self.numberInTelemetry += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=4)
              self.AdmittedToTelemetry()

      self.utilizationInZone3 = (self.numberUrgentL3/6)*100

  def handleZone4(self, numberUrgentL4, numberNonUrgentL5):
      if self.numberNonUrgentL5 + self.numberUrgentL4 < 12:
          randomValue = rn.random()
          if randomValue <= 0.25:
              self.numberInDischarge += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=5)
          elif randomValue <= 0.50:
              self.numberInOR += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=5)
              self.AdmittedToOR()
          elif randomValue <= 0.75:
              self.numberInICU += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=5)
              self.AdmittedToICU()
          else:
              self.numberInTelemetry += 1
              self.timeDepartureED = self.clock + self.GenerateServiceTime(level=5)
              self.AdmittedToTelemetry()

      self.utilizationInZone4 = (self.numberUrgentL4/12)*100

  def AdmittedToOR(self):
      self.timeArrivalOR = self.timeDepartureED
      print("A Patient Arrives into the OR")
      rand1 = rn.random()
      prob1 = rn.random()
      if (rand1<=0.5):
        # Patient has a Broken Limb
        self.timeInOR = self.timeArrivalOR + np.random.uniform(5,10)
        if (prob1<=0.8):
          # Perform an X-Ray on the Patient
          self.timeInOR = self.timeInOR + np.random.uniform(3,5)
        else:
          # Do NOT Perform an X-Ray on the Patient
          pass

        if (prob1<=0.7):
          # Perform an cast/splint on the Patient
          self.timeInOR = self.timeInOR + np.random.uniform(5,15)
        else:
          # Do NOT Perform an cast/splint on the Patient
          pass

        self.timeDepartureOR = self.timeInOR + np.random.uniform(5,10) # Time + Rest Time

      else:
        # Patient has a Lacteration
        self.timeInOR = self.timeArrivalOR + 2
        if (prob1<=0.75):
          # Perform an stitches on the Patient
          self.timeInOR = self.timeInOR + np.random.triangular(10,15,25)
        else:
          # Do NOT Perform an stitches on the Patient
          pass

        if (prob1<=0.3):
          # Perform an tetnus shot on the Patient
          self.timeInOR = self.timeInOR + np.random.uniform(2,5)
        else:
          # Do NOT Perform an tetnus shot on the Patient
          pass

        self.timeDepartureOR = self.timeInOR + np.random.uniform(10,15) # Time + Rest Time

      self.numberDeparture += 1
      self.utilizationInOR = (self.numberInOR/22)*100
      print("A Patient Departs from the OR")

  def AdmittedToICU(self):
      self.timeArrivalICU = self.timeDepartureED
      print("A Patient Arrives into the ICU")
      rand2 = rn.random()
      prob2 = rn.random()
      if (rand2<=0.25):
        # Patient has Trauma:
        self.timeInICU = self.timeArrivalICU + np.random.uniform(5,12)
        if (prob2<=0.9):
          # Perform an X-Ray on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(3,5)
        else:
          # Do NOT Perform an X-Ray on the Patient
          pass
        if (prob2<=0.8):
          # Perform an Surgery Type A on the Patient
          self.timeInICU = self.timeInICU + np.random.triangular(10,25,50)
        else:
          # Do NOT Perform an Surgery Type A on the Patient
          pass

        self.timeDepartureICU = self.timeInICU + np.random.uniform(2,10)

      elif (rand2 <= 0.5):
        # Patient had Cardiac Arrest
        self.timeInICU= self.timeArrivalICU + np.random.uniform(2,5)
        if (prob2<=0.95):
          # Perform an ECU on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(7,10)
        else:
          # Do NOT Perform an ECU on the Patient
          pass
        if (prob2<=0.6):
          # Perform an Surgery Type B on the Patient
          self.timeInICU = self.timeInICU + np.random.triangular(30,45,90)
        else:
          # Do NOT Perform an Surgery Type B on the Patient
          pass

        self.timeDepartureICU = self.timeInICU + np.random.uniform(2,15) # Time + Rest Time


      elif (rand2 <= 0.75):
        # Patient had a Stroke:
        self.timeInICU = self.timeArrivalICU + np.random.uniform(5,12)
        if (prob2<=0.90):
          # Perform an CT Scan on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(10,25)
        else:
          # Do NOT Perform an CT Scan on the Patient
          pass
        if (prob2<=0.8):
          # Perform an Medication on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(2,5)
        else:
          # Do NOT Perform an Medication on the Patient
          pass

        if (rn.random() <= 0.25):
          self.timeDepartureICU = self.timeInICU + np.random.uniform(5,15) # Time + Rest Time
        else:
           self.timeDepartureICU = self.timeInICU + np.random.uniform(45,50) # Time + Rest Time

      else:
        # Patient had a Severe Asthma
        self.timeInICU = self.timeArrivalICU + 2
        if (prob2<=0.90):
          # Perform an Oxygen Therapy on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(30,60)
        else:
          # Do NOT Perform an Oxygen Therapy on the Patient
          pass
        if (prob2<=0.7):
          # Perform an Nebulizer on the Patient
          self.timeInICU = self.timeInICU + np.random.uniform(2,3)
        else:
          # Do NOT Perform an Nebulizer on the Patient
          pass

        self.timeDepartureICU = self.timeInICU + np.random.uniform(15,25) # Time + Rest Time

      self.numberDeparture += 1
      self.utilizationInICU = (self.numberInICU/22)*100
      print("A Patient Departs from the ICU")

  def AdmittedToTelemetry(self):
      self.timeArrivalTelemetry = self.timeDepartureED
      print("A Patient Arrives into the Telemetry")
      rand3 = rn.random()
      prob3 = rn.random()
      if (rand3<=0.5):
        # Patient had Mild Asthma
        self.timeInTelemetry = self.timeArrivalICU + 2
        if (prob3<=0.6):
          # Perform an Nebulizer on the Patient
          self.timeInTelemetry = self.timeInTelemetry + np.random.uniform(2,3)
        else:
          # Do NOT Perform an Nebulizer on the Patient
          pass

        if (prob3<=0.3):
          # Perform an Oxygen Therapy on the Patient
          self.timeInTelemetry = self.timeInTelemetry + np.random.uniform(30,60)
        else:
          # Do NOT Perform an Oxygen Therapy on the Patient
          pass

        self.timeDepartureTelemetry = self.timeInTelemetry + np.random.uniform(5,10) # Time + Rest Time

      else:
        # Patient had a Common Cold:
        self.timeInTelemetry = self.timeArrivalICU + np.random.uniform(5,10)
        if (prob3<=0.9):
          # Perform an Medication on the Patient
          self.timeInTelemetry = self.timeInTelemetry + np.random.uniform(2,5)
        else:
          # Do NOT Perform an Medication on the Patient
          pass

        self.timeDepartureTelemetry = self.timeInTelemetry + 5 # Time + Rest Time
        self.numberDeparture += 1

      self.numberDeparture += 1
      self.utilzationInTelemetry = (self.numberInTelemetry/22)*100
      print("A Patient Departs from the Telemetry")

  def GenerateInterarrivalTime(self):
      return np.random.exponential(0.22)

  def GenerateServiceTime(self, level):
    if (level == 1):
      return 0
    elif (level == 2 or level == 3):
      return np.random.uniform(0.75, 2.25)
    elif (level == 4 and level == 5):
      return np.random.uniform(7.5, 11.25)
    else:
      return np.random.exponential(1./8)

np.random.seed(0)

s = Simulation()

for i in range (100):
  print(" ")
  print("Event #: " + str(i))
  print("-------------------------------------------")
  s.advanceTime()
  print(s.advanceTime)
  print("----- Time Statistics -----")
  print("Time on Clock (hours): " + str(s.clock))
  print("Time of Current Event (hours): " + str(s.timeEvent))
  print("----- Total Count Statistics -----")
  print("Total Number of Arrivals in the System: " + str(s.numberArrivals))
  print("Total Number of Departures in the System: " + str(s.numberDeparture))
  print("Total Number of Patients in the ED: " + str(s.numberInED))
  print("Total Number of Patients in the OR: " + str(s.numberInOR))
  print("Total Number of Patients in the ICU: " + str(s.numberInICU))
  print("Total Number of Patients in the Telemetry: " + str(s.numberInTelemetry))
  print("Total Number of Patients Gone Through System: " + str(s.numberInSystem))
  print("Total Number of Patients Currently In System: " + str((s.numberArrivals - s.numberDeparture)))
  print("Total Number of Ambulences Diverted: " + str(s.numberAmbulenceDiverted))
  print("Total Wait Time in System (All Patients): " + str(s.totalWait))
  if(s.numberInSystem != 0):
    print("Average Wait Time in System: " + str(s.totalWait/s.numberInSystem))
  else:
    print("Average Wait Time in System: 0")
  print("----- Total Utilization Statistics -----")
  print("Total Utilization of ED (%): " + str(s.utilizationInED))
  print("Total Utilization of Zone1 (%): " + str(s.utilizationInZone1))
  print("Total Utilization of Zone2 (%): " + str(s.utilizationInZone2))
  print("Total Utilization of Zone3 (%): " + str(s.utilizationInZone3))
  print("Total Utilization of Zone4 (%): " + str(s.utilizationInZone4))
  print("Total Utilization of OR (%): " + str(s.utilizationInOR))
  print("Total Utilization of ICU (%): " + str(s.utilizationInICU))
  print("Total Utilization of Telemetry (%): " + str(s.utilzationInTelemetry))
  print("----- Future Event Scheduling -----")
  print("Next Scheduled Arrival Time for Walk In: " + str(s.timeArrivalWalkIn))
  print("Next Scheduled Arrival Time for Ambulence: " + str(s.timeArrivalAmbulence))
  print("Next Scheduled Arrival Time for OR: " + str(s.timeArrivalOR))
  print("Next Scheduled Arrival Time for ICU: " + str(s.timeArrivalICU))
  print("Next Scheduled Arrival Time for Telemetry: " + str(s.timeArrivalTelemetry))
  print("Next Scheduled Departure Time for ED: " + str(s.timeDepartureED))
  print("Next Scheduled Departure Time for OR: " + str(s.timeDepartureOR))
  print("Next Scheduled Departure Time for ICU: " + str(s.timeDepartureICU))
  print("Next Scheduled Departure Time for Telemetry: " + str(s.timeDepartureTelemetry))
  print("-------------------------------------------")
  print(" ")