import PySimpleGUI as sg
from garden import GardenProduct


# izveido plauktu, kur viss tiks attēlots
pantry = []

# iesāc izvēlnes priekš džema produktiem un rediģēt/izdzēst kā nekas sākumā
jam_product_dropdown = None
edit_product_dropdown = None
delete_product_dropdown = None

# funkcija lai darbotos dropdown
def update_dropdowns():
    product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry]  # Include Jam items
    jam_product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry if item.product_type != "Ievārījums"]
    edit_product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry]  # Include jams in edit and delete dropdowns
    jam_product_dropdown.update(values=jam_product_list)
    edit_product_dropdown.update(values=edit_product_list)
    delete_product_dropdown.update(values=edit_product_list)  # Same as edit dropdown

# Izveido GUI noformējumu
layout = [
    [sg.Text("Vecmāmiņai")],
    [sg.TabGroup([
        [sg.Tab("Pievienot Ražu", [
            [sg.Text("Produkta Nosaukums:"), sg.InputText(key="name")],
            [sg.Text("Daudzums (kg):"), sg.InputText(key="quantity")],
            [sg.Text("Tips:"), sg.Radio("Auglis", "RADIO1", default=True, key="fruit"), sg.Radio("Dārzeņi", "RADIO1", key="vegetable")],
            [sg.Text("Šķirne (ja piemērojams):"), sg.InputText(key="variety")],
            [sg.Button("Pievienot Ražu")]
        ])],
        [sg.Tab("Izveidot Ievārījumu", [
            [sg.Text("Izvēlieties produktu Ievārījumam:")],
            [sg.Combo([], key="jam_product", readonly=True, size=(40, 6))],  # Adjust the size here
            [sg.Text("Ievārījuma Daudzums (kg):"), sg.InputText(key="jam_quantity")],
            [sg.Button("Izveidot Ievārījumu")]
        ])],
        [sg.Tab("Rediģēt/Dzēst", [
            [sg.Text("Izvēlieties produktu Rediģēšanai:")],
            [sg.Combo([], key="edit_product", readonly=True, size=(40, 6))],  # Adjust the size here
            [sg.Text("Jaunais Nosaukums:"), sg.InputText(key="new_name")],
            [sg.Text("Jaunais Daudzums (kg):"), sg.InputText(key="new_quantity")],
            [sg.Text("Jaunais Tips:"), sg.Radio("Auglis", "RADIO2", default=True, key="new_fruit"), sg.Radio("Dārzeņi", "RADIO2", key="new_vegetable")],
            [sg.Text("Jaunā Šķirne (ja piemērojams):"), sg.InputText(key="new_variety")],
            [sg.Button("Rediģēt")],
            [sg.Text("Izvēlieties produktu Dzēšanai:")],
            [sg.Combo([], key="delete_product", readonly=True, size=(40, 6))],  # Adjust the size here
            [sg.Button("Dzēst")]
        ])]
    ])],
    [sg.Text("Pārtikas Skapis:")],
    [sg.Listbox([], size=(50, 6), key="inventory_list")],
    [sg.Button("Iziet")]
]

# izveido window
window = sg.Window("Vecmāmiņai mīļajai", layout)

while True:
    try:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break

        if event == "Pievienot Ražu":
            name = values["name"] if values["name"] else "produkts"
            quantity = float(values["quantity"]) if values["quantity"] else 0
            product_type = "Auglis" if values["fruit"] else "Dārzenis"
            variety = values["variety"] if values["variety"] else " "

            pantry.append(GardenProduct(name, quantity, product_type, variety))
            sg.popup(f"Raža pievienota: {name} ({quantity} kg)")

            # izveido sarakstā lietas ar numuriem sākumā
            inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
            window["inventory_list"].update(inventory_list)

            # iesāc dropdowns ja vēl nav nekā
            if jam_product_dropdown is None:
                jam_product_dropdown = window["jam_product"]
            if edit_product_dropdown is None:
                edit_product_dropdown = window["edit_product"]
            if delete_product_dropdown is None:
                delete_product_dropdown = window["delete_product"]

            # ievadi jauno info no sarkasta dropdownos
            update_dropdowns()

        if event == "Izveidot Ievārījumu":
            jam_product_name = values["jam_product"]
            jam_quantity = float(values["jam_quantity"])

            for item in pantry:
                if f"{item.name} ({item.variety}) ({item.product_type})" == jam_product_name:
                    if item.product_type == "Dārzenis":
                        sg.popup("Ievārījumu no dārzeņiem nevar izveidot") #kas parādās ja centies izveidot ievārījumu no dārzeņiem
                    else:
                        jam = item.make_jam(jam_quantity)
                        if jam:
                            pantry.append(jam)
                            sg.popup(f"Ievārījums izveidots: {jam_product_name} ({jam_quantity} kg)")
                        else:
                            sg.popup(f"Nepietiek {jam_product_name} pārtikas skapī, lai izveidotu ievārījumu")
                    break
            else:
                sg.popup(f"{jam_product_name} nav atrasts pārtikas skapī.")

            # atjaunini sarakstu ar numuriem
            inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
            window["inventory_list"].update(inventory_list)

        if event == "Rediģēt":
            edit_product_name = values["edit_product"]

            for item in pantry:
                if f"{item.name} ({item.variety}) ({item.product_type})" == edit_product_name:
                    new_name = values["new_name"] if values["new_name"] else item.name
                    new_quantity = float(values["new_quantity"]) if values["new_quantity"] else item.quantity
                    new_product_type = "Auglis" if values["new_fruit"] else "Dārzenis"
                    new_variety = values["new_variety"] if values["new_variety"] else item.variety

                    item.name = new_name
                    item.quantity = new_quantity
                    item.product_type = new_product_type
                    item.variety = new_variety
                    sg.popup(f"Produkts atjaunināts: {new_name} ({new_quantity} kg)")

                 
                    inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
                    window["inventory_list"].update(inventory_list)

                    # atjaunini lai dropdowni parāda rediģētos produktus
                    update_dropdowns()
                    break
            else:
                sg.popup(f"{edit_product_name} nav atrasts pārtikas skapī.")

        if event == "Dzēst":
            delete_product_name = values["delete_product"]

            for item in pantry:
                if f"{item.name} ({item.variety}) ({item.product_type})" == delete_product_name:
                    pantry.remove(item)
                    sg.popup(f"{delete_product_name} dzēsts no pārtikas skapja.")
                    break
            else:
                sg.popup(f"{delete_product_name} nav atrasts pārtikas skapī.")

           
            inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
            window["inventory_list"].update(inventory_list)

            # atjaunini dropdownus lai neiekļautu izdzēstus produktus
            update_dropdowns()
    except Exception as e:
        sg.popup_error(f"Notika kļūda: {e}")

window.close()
