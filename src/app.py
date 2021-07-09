import time

import gce
import fileManager

gce_water = gce.find_first_gce()
gce_water_data = gce.donnees(gce_water)
gce_compteur = gce.compteurs(gce_water)

if (gce_water is None):
    # print("gce_water is None")
    gce_ip, gce_nom, gce_mac, gce_port = None, None, None, None
    gce_index_total, gce_index_jour = None, None
    # raise
else:
    gce_ip, gce_nom, gce_mac, gce_port = gce_water
    gce_index_total = gce_water_data["INDEX_C1"]
    gce_index_jour = gce_compteur["Day_C1"]

# def job():
#     print("I'm working...")
#     time.sleep(5)


if __name__ == "__main__":
    # execute only if run as a script
    print(" Index jour :", gce_index_jour, "\nIndex total :", gce_index_total)
    # print(gce_port)
    # print(gce_water)
    # print("\ndonnees() :")
    # print(donnees(gce_water))
    # print("\ncompteurs() :")
    # print(compteurs(gce_water))
    # print("Done")
