import schedule
import time

from gce import *

gce_water = find_first_gce()
gce_water_data = donnees(gce_water)
gce_compteur = compteurs(gce_water)

gce_ip, gce_nom, gce_mac, gce_port = gce_water

gce_index_total = gce_water_data["INDEX_C1"]

gce_index_jour = gce_compteur["Day_C1"]

# def job():
#     print("I'm working...")


# schedule.every(5).seconds.do(job)

# while True:
#     schedule.run_pending()
#     # time.sleep(1)


if __name__ == "__main__":
    # execute only if run as a script
    print(gce_index_jour, gce_index_total)
    # print(gce_port)
    # print(gce_water)
    # print("\ndonnees() :")
    # print(donnees(gce_water))
    # print("\ncompteurs() :")
    # print(compteurs(gce_water))
    print("Done")
