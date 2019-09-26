module.exports = {
    id: 'jdb_entreprise',
    label: 'Journal de bord Entreprise',
    name: 'Journal de bord Entreprise',
    namePlural: 'Journeaux de bord Entreprise',
    icon: 'todo.gif',
    titleField: 'id_internal',
    fields: [{
        id: 'andi_id',
        label: 'Identifiant ANDi',
        type: 'text',
        readOnly: true,
        required: true,
        inMany: true,
        width: 50,
        maxLength: 120,
    }, {
        id: 'date',
        label: 'Jour concerné',
        inMany: true,
        type: 'date',
        width: 50,
    }, {
        id: 'utilisation_outils_it',
        label: 'Utilisation outils IT',
        inMany: false,
        type: 'lov'
        list: [
            { 'id': 'oui', 'text': 'Oui' },
            { 'id': 'non', 'text': 'Non' },
        ],
        width: 100,
    }, {
        id: 'faits',
        label: 'Faits marquants',
        type: 'textmultiline',
        inMany: false,
        width: 100,
    }, {
        id: 'difficultes',
        label: 'Difficultés particulières',
        type: 'textmultiline',
        inMany: false,
        width: 100,
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
        label: 'Journal de Bord Entreprise',
        width: 100,
        fields: ['utilisation_outils_it', 'faits', 'difficultes']
    }
    ]
}
