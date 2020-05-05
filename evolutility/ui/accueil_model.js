module.exports = {
        id: "accueil",
        label: "ANDi Accueil Entreprises",
        name: "ANDi Accueil",
        namePlural: "ANDi Accueil",
        icon: "todo.gif",
        titleField: "id_internal",

        fields: [ {
        //////////////// COMPANY_DATA
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
            type: 'integer',
            width: 40,
            maxLength: 14,
            inMany: true
        }, {
            id: 'acces',
            label: 'Acces',
            type: 'lov',
            list: [
                { 'id': 'train', 'text':'Train'},
                { 'id': 'rer','text': 'RER'},
                { 'id': 'metro', 'text':'Metro'},
                { 'id': 'bus', 'text':'Bus'}, 
                { 'id': 'tram', 'text':'Tram'},
                { 'id': 'parking_pmr', 'text':'Parking accessible PMR'},
                { 'id': 'autre', 'text':'Autre'}
            ],
            inMany: true,
            width: 20,
        }
        ]
}
