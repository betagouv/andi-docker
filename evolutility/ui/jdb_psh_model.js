module.exports = {
    id: 'jdb_psh',
    label: 'Journal de bord PSH',
    name: 'Journal de bord PSH',
    namePlural: 'Journeaux de bord PSH',
    icon: 'todo.gif',
    titleField: 'id_internal',
    fields: [{
        id: 'andi_id',
        label: 'ANDi iD',
        type: 'text',
        required: true,
        readOnly: true,
        inMany: true,
        width:50,
        maxLength: 120,
    }, {
        id: 'date',
        type: 'date',
        label: 'Jour concerné',
        required: true,
        inMany: true,
        width:50,
        maxLength: 120,
    }, {
        id: 'activites_semaines',
        type: 'textmultiline'
        label: 'Activités semaine',
        inMany: false,
        required: true,
        width:100,
    }, {
        id: 'utilisation_outils_it',
        label: 'Utilisation outils IT',
        inMany: false,
        required: true,
        type: 'lov'
        list: [
            { 'id': 'oui', 'text': 'Oui' },
            { 'id': 'non', 'text': 'Non' },
        ],
        width:100,
    }, {
        id: 'evenements_plu',
        type: 'textmultiline'
        label: 'Événements qui ont plu',
        inMany: false,
        required: true,
        width:100,
    }, {
        id: 'evenements_deplu',
        type: 'textmultiline',
        label: 'Événements qui ont deplu',
        inMany: false,
        required: true,
        width:100,
    }],

    groups: [{
        id: 'metadata',
        type: 'panel',
        label: 'Données',
        width: 100,
        fields: ['andi_id', 'date']
    }, {
        id: 'data',
        type: 'panel',
        label: 'Journal de Bord PSH',
        width: 100,
        fields: ['activites_semaines', 'utilisation_outils_it', 'evenements_plu', 'evenements_deplu']
    }
    ]
}
