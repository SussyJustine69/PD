import PySimpleGUI as sg
from garden import GardenProduct
sg.theme('LightBrown5')

# izveido plauktu, kur viss tiks attēlots
pantry = []

# iesāc izvēlnes priekš džema produktiem un rediģēt/izdzēst kā nekas sākumā
jam_product_dropdown = None
edit_product_dropdown = None
delete_product_dropdown = None

# funkcija lai darbotos dropdown
def update_dropdowns():
    product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry]  # Iekļauj ievārījumus
    jam_product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry if item.product_type != "Ievārījums"]
    edit_product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry if item.product_type != "Ievārījums"] 
    delete_product_list = [f"{item.name} ({item.variety}) ({item.product_type})" for item in pantry]  # Iekļauj ievārījumus izdzēšanas opcijā
    jam_product_dropdown.update(values=jam_product_list)
    edit_product_dropdown.update(values=edit_product_list)
    delete_product_dropdown.update(values=delete_product_list)

# Izveido GUI noformējumu
layout = [
    [sg.Text("Vecmāmiņai")],
    [sg.TabGroup([
        [sg.Tab("Pievienot Ražu", [
            [sg.Text("Produkta Nosaukums:"), sg.InputText(key="name")],
            [sg.Text("Daudzums (kg):"), sg.InputText(key="quantity")],
            [sg.Text("Tips:"), sg.Radio("Auglis", "RADIO1", default=True, key="fruit"), sg.Radio("Dārzeņi", "RADIO1", key="vegetable")],
            [sg.Text("Šķirne (āboliem):"), sg.InputText(key="variety")],
            [sg.Button("Pievienot Ražu")]
        ])],
        [sg.Tab("Izveidot Ievārījumu", [
            [sg.Text("Izvēlieties produktu Ievārījumam:")],
            [sg.Combo([], key="jam_product", readonly=True, size=(40, 6))],
            [sg.Text("Ievārījuma Daudzums (kg):"), sg.InputText(key="jam_quantity")],
            [sg.Button("Izveidot Ievārījumu")]
        ])],
        [sg.Tab("Rediģēt/Dzēst(Apēst)", [
            [sg.Text("Izvēlieties produktu Rediģēšanai(Apēšanai):")],
            [sg.Combo([], key="edit_product", readonly=True, size=(40, 6))],
            [sg.Text("Jaunais Nosaukums:"), sg.InputText(key="new_name")],
            [sg.Text("Jaunais Daudzums (kg):"), sg.InputText(key="new_quantity")],
            [sg.Text("Jaunais Tips:"), sg.Radio("Auglis", "RADIO2", default=True, key="new_fruit"), sg.Radio("Dārzeņi", "RADIO2", key="new_vegetable")],
            [sg.Text("Jaunā Šķirne (āboliem):"), sg.InputText(key="new_variety")],
            [sg.Button("Rediģēt")],
            [sg.Text("Izvēlieties produktu Dzēšanai:")],
            [sg.Combo([], key="delete_product", readonly=True, size=(40, 6))],
            [sg.Button("Dzēst")]
        ])]
    ])],
    [sg.Text("Pārtikas Skapis:")],
    [sg.Listbox([], size=(50, 6), key="inventory_list")],
    
]

# izveido window
window = sg.Window("Vecmāmiņai mīļajai", layout)

while True:
    try:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == "Pievienot Ražu":
            name = values["name"].strip()
            quantity = values["quantity"].strip()
            
            # Pārbaude vai lauki nav tukši
            if not name:
                sg.popup("Produkta nosaukums nav ievadīts")
            elif not quantity:
                sg.popup("Daudzums nav ievadīts")
            else:
                quantity = float(quantity)
                product_type = "Auglis" if values["fruit"] else "Dārzenis"
                variety = values["variety"].strip()

                pantry.append(GardenProduct(name, quantity, product_type, variety))
                sg.popup(f"Raža pievienota: {name} ({quantity} kg)")

                # izveido sarakstā lietas ar numuriem sākumā
                inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
                window["inventory_list"].update(inventory_list)

                # iesāk dropdownu ja vēl nav nekā
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
            jam_quantity = values["jam_quantity"].strip()
            
            # Pārbaude vai lauki nav tukši
            if not jam_product_name:
                sg.popup("Nav izvēlēts produkts Ievārījumam")
            elif not jam_quantity:
                sg.popup("Ievadiet Ievārījuma daudzumu")
            else:
                jam_quantity = float(jam_quantity)
                update_dropdowns()
                for item in pantry:
                    if f"{item.name} ({item.variety}) ({item.product_type})" == jam_product_name:
                        if item.product_type == "Dārzenis":
                            sg.popup("Ievārījumu no dārzeņiem nevar izveidot")  # kas parādās ja centies izveidot ievārījumu no dārzeņiem
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
                update_dropdowns()

        if event == "Rediģēt":
            edit_product_name = values["edit_product"] #TURPMĀKAIS KODS NODROŠINA PRODUKTU REDIĢĒŠANU

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
                    sg.popup(f"Produkts atjaunināts: {new_name} ({new_quantity} kg)") #PARĀDĀS KAD REDIĢĒTS PRODUKTS

                 
                    inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)]
                    window["inventory_list"].update(inventory_list) #updato listiņu ar rediģēto produktu

                    # atjaunini lai dropdowni parāda rediģētos produktus
                    update_dropdowns()
                    break
            else:
                sg.popup(f"{edit_product_name} nav atrasts pārtikas skapī.")

        if event == "Dzēst":
            delete_product_name = values["delete_product"] 

            for item in pantry:
                if f"{item.name} ({item.variety}) ({item.product_type})" == delete_product_name:
                    pantry.remove(item) #izdara, lai tiek izdzēsts specifiskais produkts
                    sg.popup(f"{delete_product_name} dzēsts no pārtikas skapja.") 
                    break
            else:
                sg.popup(f"{delete_product_name} nav atrasts pārtikas skapī.") #šis kods parādās, ja nav izvēlēts vai nav korekts produkts atrasts listiņā

           
            inventory_list = [f"{i+1}. {item.name} ({item.variety}) ({item.product_type}) ({item.quantity} kg)" for i, item in enumerate(pantry)] #salabo korekti numurāciju, ja izdzēsts produkts no listiņa
            window["inventory_list"].update(inventory_list) #updato listiņu, lai nerādītu izdzēstos produktus

            # atjaunini dropdownus lai neiekļautu izdzēstus produktus
            update_dropdowns()
    except Exception as e:
        sg.popup_error(f"Notika kļūda: {e}")

window.close()

