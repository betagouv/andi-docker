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
        width:30,
        maxLength: 120,
    }, {
        id: 'date',
        type: 'date',
        label: 'Jour concerné',
        required: true,
        inMany: true,
        width:30,
        maxLength: 120,
    }, {
        id: 'activites_semaines',
        type: 'text'
        label: 'Activités semaine',
        inMany: false,
        required: true,
        width:30,
        maxLength: 120,
    }, {
        id: 'utilisation_outils_it',
        type: 'lov'
        label: 'Utilisation outils IT',
        inMany: false,
        required: true,
        list: [
            { 'id': 'oui', 'text': 'Oui' },
            { 'id': 'non', 'text': 'Non' },
        ],
        width:30,
        maxLength: 120,
    }, {
        id: 'evenements_plu',
        type: 'text'
        label: 'Événements qui ont plu',
        inMany: false,
        required: true,
        width:30,
        maxLength: 120,
    }, {
        id: 'evenements_plu',
        type: 'text'
        label: 'Événements qui ont deplu',
        inMany: false,
        required: true,
        width:30,
        maxLength: 120,
    }]
}
