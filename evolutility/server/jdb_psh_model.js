module.exports = {
    id: 'jdb_psh',
    active: true,
    table: 'form_jdb_psh',
    pKey: 'id_internal',
    title: 'Journal de bord PSH',
    titleField: 'id_internal',
    searchFields: ['andi_id', 'date'],
    fields: [{
        id: 'andi_id',
        column: 'id_andi',
        type: 'text',
        label: 'Identifiant ANDi',
        readOnly: true,
        inMany: true,
    }, {
        id: 'date',
        column: 'date_day',
        type: 'date',
        label: 'Jour concerné',
        inMany: true,
    }, {
        id: 'activites_semaines',
        column: 'activites_semaines',
        type: 'text',
        label: 'Activités semaine',
        inMany: false,
    }, {
        id: 'utilisation_outils_it',
        column: 'utilisation_outils_it',
        type: 'lov',
        lovTable: 'lov_ouinon',
        label: 'Utilisation outils IT',
        inMany: false,
    }, {
        id: 'evenements_plu',
        column: 'evenements_plu',
        type: 'text',
        label: 'Événements qui ont plu',
        inMany: false,
    }, {
        id: 'evenements_deplu',
        column: 'evenements_deplu',
        type: 'text',
        label: 'Événements qui ont deplu',
        inMany: false,
    }]
}
