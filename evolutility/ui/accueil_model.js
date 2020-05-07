module.exports = {
        id: "accueil",
        label: "ANDi Accueil Entreprises",
        name: "ANDi Accueil",
        namePlural: "ANDi Accueil",
        icon: "todo.gif",
        titleField: "id_internal",

        fields: [ {
        //////////////// Entreprise
            id: 'id',
            label: 'Identifiant',
            type: 'integer',
            width: 20,
            maxLength: 11,
            readOnly: true,
            help: 'Identifiant interne',
        }, {
            id: 'siren',
            label: 'Siren',
            type: 'string',
            width: 40,
            maxLength: 14,
            inMany: true
        }, {
            id: 'siret',
            label: 'Siret',
            type: 'textmultiline',
            width: 50,
        }, {
        //////////////// Contact
            id: 'contact_nom',
            label: 'Nom',
            type: 'text',
            width: 30,
        }, {
            id: 'contact_fonction',
            label: 'Fonction',
            type: 'text',
            width: 10,
        }, {
            id: 'contact_phone',
            label: 'Téléphone',
            type: 'text',
            width: 20,
        }, {
            id: 'contact_mail',
            label: 'Email',
            type: 'text',
            width: 40,
        }, {
        //////////////// Referent
            id: 'ref_nom',
            label: 'Nom',
            type: 'text',
            width: 30,
        }, {
            id: 'ref_phone',
            label: 'Téléphone',
            type: 'text',
            width: 20,
        }, {
            id: 'ref_mail',
            label: 'Email',
            type: 'text',
            width: 40,
        }, {
        //////////////// Acceuil
            id: 'couverture',
            type: 'lov',
            lovTable: 'lov_couverture',
            list: [
                {'id': 'un', 'text': 'Un'},
                {'id': 'tous', 'text': 'Tous'},
                {'id': 'tous_departement', 'text': 'Département'},
                {'id': 'tous_region', 'text': 'Région'},
                {'id': 'specifique_dep', 'text': 'Départements indiquées'},
                {'id': 'specifique_regions', 'text': 'Regions indiquées'},
                {'id': 'autre', 'text': 'Autre'}
            ],
            label: 'Couverture',
            readOnly: false,
            width: 40,
        }, {
            id: 'couverture_meta',
            type: 'textmultiline',
            label: 'Couverture - Autre',
            width: 50,
        }, {
            id: 'acces',
            type: 'list',
            list: [
                {'id': 'train', 'text':'Train'},
                {'id': 'rer','text': 'RER'},
                {'id': 'metro', 'text':'Metro'},
                {'id': 'bus', 'text':'Bus'}, 
                {'id': 'tram', 'text':'Tram'},
                {'id': 'parking_pmr', 'text':'Parking accessible PMR'},
                {'id': 'autre', 'text':'Autre'}
            ],
            label: 'Accès',
            inMany: true,
            width: 40
        }, {
            id: 'acces_meta',
            type: 'textmultiline',
            label: 'Accès - Autre',
            width: 50,
        }, {
            id: 'accueil_pmr',
            type: 'boolean',
            label: 'Accueil PMR'
        }, {
            id: 'pmr',
            type: 'list',
            list: [
                {'id': 'plain_pied', 'text':'Accès de plain pied'},
                {'id': 'portes_automatiques', 'text': 'Portes automatiques'},
                {'id': 'portes_larges', 'text': 'Portes larges'},
                {'id': 'ascenseurs', 'text': 'Ascenseurs'},
                {'id': 'sanitaires_pmr', 'text': 'Sanitaires PMR'},
                {'id': 'rampes_access', 'text': 'Rampes d`accès'},
                {'id': 'restaurant_pmr', 'text': 'Restaurant PMR'},
                {'id': 'elevateur', 'text': 'Élévateur'},
                {'id': 'autre', 'text': 'Autre'}
            ],
            label: 'PMR',
            readOnly: false,
            width: 70,
        }, {
            id: 'pmr_meta',
            type: 'textmultiline',
            label: 'PMR - Autre',
            width: 70,
        }, {
            id: 'amenagement',
            type: 'list',
            list: [
                {'id': 'boucle_magneto', 'text': 'Boucles magnétiques'},
                {'id': 'bandes_pododactiles', 'text': 'Bandes pterodactiles'},
                {'id': 'ascenseurs_vocalises', 'text': 'Acenseurs vocalisés'},
                {'id': 'autre', 'text': 'Autre'}
            ],
            label: 'Aménagements',
            readOnly: false,
            width: 70,
        }, {
            id: 'amenagement_meta',
            type: 'textmultiline',
            label: 'Aménagements - Autre'
        }, {
            id: 'materiel',
            type: 'list',
            list: [
                {'id': 'bureaux_postes_pmr', 'text': 'Bureaux et postes adaptés PMR'},
                {'id': 'fauteuils_ergo', 'text': 'Fauteuil(s) ergonomique(s)'},
                {'id': 'aides_visuel', 'text': 'Outils bureautiques et/ou techniques déficience visuelle'},
                {'id': 'aides_auditif', 'text': 'Outils bureautiques et/ou techniques déficience auditive'},
                {'id': 'aides_dyslexie', 'text': 'Outils bureautiques et/ou techniques personnes dyslexiques'},
                {'id': 'autre', 'text': 'Autre'}
            ],
            label: 'Matériel',
            readOnly: false
        }, {
            id: 'materiel_meta',
            type: 'textmultiline',
            label: 'Matériel - Autre'
        }, {
            id: 'plateforme',
            type: 'boolean',
            label: 'Collaboration Plateforme'
        }, {
            id: 'plateforme_nom',
            type: 'text',
            label: 'Nom Plateforme'
        }
        ],

        //////////////// Groupes
        groups: [{
          id: 'company_data',
            type: 'panel',
            label: 'Données Entreprise',
            width: 100,
            fields: [
                'id', 'siren', 'siret'
            ]
        }, {
          id: 'contact_data',
            type: 'panel',
            label: 'Contact',
            width: 50,
            fields: [
              'contact_nom', 'contact_fonction',
              'contact_phone', 'contact_mail',
            ]
        },{
          id: 'ref_data',
            type: 'panel',
            label: 'Référant',
            width: 50,
            fields: [
              'ref_nom', 'ref_fonction',
              'ref_phone', 'ref_mail',
            ]
        },{
          id: 'accueil_data',
            type: 'pane',
            label: 'Accueil',
            width: 100,
            fields : [
              'couverture', 'couverture_meta',
              'acces', 'acces_meta', 'accueil_pmr',
              'pmr', 'pmr_meta', 'amenagement',
              'materiel', 'materiel_meta',
              'plateforme', 'plateforme_nom'
            ]
        }]
}
