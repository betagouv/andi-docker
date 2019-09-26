module.exports = {
    id: 'jdb_entreprise',
    active: true,
    table: 'form_jdb_psh',
    pKey: 'id_internal',
    title: 'Journal de bord Entreprise',
    titleField: 'id_internal',
    searchFields: [],
    fields: [{
        id: 'andi_id',
        column: 'andi_id',
        type: 'text',
        label: 'Identifiant ANDi',
        readOnly: true
    }, {
        id: 'date',
        column: 'date_day',
        type: 'date',
        label: 'Jour concerné',
        inMany: true,
    }, {
        id: 'utilisation_outils_it',
        column: 'utilisation_outils_it',
        type: 'text',
        label: 'Utilisation outils IT',
        inMany: false,
    }, {
        id: 'faits',
        column: 'faits',
        type: 'text',
        label: 'Faits marquants',
        inMany: false,
    }, {
        id: 'difficultes',
        column: 'difficultes',
        type: 'text',
        label: 'Difficultés particulières',
        inMany: false,
    }]
}
