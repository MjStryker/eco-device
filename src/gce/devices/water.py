import gce.main as gce


def get_water_info():
    gce_water = gce.find_first_gce()

    gce_ip, gce_nom, gce_mac, gce_port = None, None, None, None

    if (gce_water is not None):
        gce_ip, gce_nom, gce_mac, gce_port = gce_water

    return [gce_ip, gce_nom, gce_mac, gce_port]


def get_water_indexes():
    gce_water = gce.find_first_gce()
    gce_water_data = gce.donnees(gce_water)
    gce_compteur = gce.compteurs(gce_water)

    gce_index_total, gce_index_jour = None, None

    if (gce_water is not None):
        gce_index_total: int = gce_water_data["INDEX_C1"]
        gce_index_jour: int = gce_compteur["Day_C1"]

    return [gce_index_jour, gce_index_total]


if __name__ == "__main__":
    gce_index_jour, gce_index_total = get_water_indexes()
    print(" Index jour :", gce_index_jour, "\nIndex total :", gce_index_total)
