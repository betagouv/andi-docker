module.exports = {
    id: 'jdb_entreprise',
    active: true,
    table: 'form_jdb_entreprise',
    pKey: 'id_internal',
    title: 'Journal de bord Entreprise',
    titleField: 'id_internal',
    searchFields: [],
    fields: [{
        id: 'andi_id',
        column: 'id_andi',
        type: 'text',
        label: 'Identifiant ANDi',
        inMany: true,
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
        type: 'lov',
        lovTable: 'lov_ouinon',
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
