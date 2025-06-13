from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Chemin vers le fichier CSV
csv_file = "Avis_clients.csv"

# Fonction pour enregistrer les données dans le fichier CSV
def enregistrer_donnees(nom, pv_projet1, pv_projet2, pv_projet3):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nom complet', 'Avis du Projet 1', 'Avis du Projet 2', 'Avis du Projet 3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Si le fichier est vide, écrire les en-têtes
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerow({'Nom complet': nom, 'Avis du Projet 1': pv_projet1, 'Avis du Projet 2': pv_projet2, 'Avis du Projet 3': pv_projet3})

# Route pour le formulaire
@app.route('/', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        nom = request.form['nom']
        pv_projet1 = request.form['pv_projet1']
        pv_projet2 = request.form['pv_projet2']
        pv_projet3 = request.form['pv_projet3']
        
        enregistrer_donnees(nom, pv_projet1, pv_projet2, pv_projet3)
        
    

        
        return '''<div style="text-align: center; 
                    font-size: 18px; 
                    background-color: #4CAF50; /* Couleur de fond vert */
                    color: white; /* Couleur du texte blanc */
                    padding: 20px; /* Marge intérieure de 20px */
                    border-radius: 10px; /* Coins arrondis de 10px */
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Ombre légère */
                    margin: 20px auto; /* Centrage horizontal avec une marge externe de 20px */
                    max-width: 400px; /* Largeur maximale de 400px */
                    ">
                Données enregistrées avec succès !
                </div>'''
    return render_template('formulaire.html')

if __name__ == '__main__':
    app.run(debug=True)
