import gce.main as gce


def get_water_info():
    gce_water = gce.find_first_gce()

    gce_ip, gce_nom, gce_mac, gce_port = None, None, None, None

    if (gce_water is not None):
        gce_ip, gce_nom, gce_mac, gce_port = gce_water

    return [gce_ip, gce_nom, gce_mac, gce_port]


first_gce_device = gce.find_first_gce()


def get_water_indexes():
    gce_water = first_gce_device
    if (gce_water is None):
        gce_water = gce.find_first_gce()
    gce_water_data = gce.donnees(gce_water)
    gce_compteur = gce.compteurs(gce_water)

    water_counter_index, water_daily_consumption = None, None

    if (gce_water is not None):
        water_counter_index: int = gce_water_data["INDEX_C1"]
        water_daily_consumption: int = gce_compteur["Day_C1"]

    return [water_daily_consumption, water_counter_index]


if __name__ == "__main__":
    water_daily_consumption, water_counter_index = get_water_indexes()
    print(" Index jour :", water_daily_consumption,
          "\nIndex total :", water_counter_index)
