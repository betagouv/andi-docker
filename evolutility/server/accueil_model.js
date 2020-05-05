module.exports = {
    id: 'accueil',
    active: true,
    table: 'andi_accueil',
    pKey: 'id_internal',
    title: 'andi_accueil',
    titleField: 'id_internal',
    searchFields: ['siret', 'siren', 'ref_nom', 'contact_nom'],
    fields: [{
        id: 'siren',
        column: 'siren',
        type: 'integer',
        label: 'identifiant',
        readOnly: true,
        inMany: true
    }, {
        id: 'ref_nom',
        column: 'ref_nom',
        type: 'text',
        label: 'Référant Nom',
        inMany: true
    }, {
        id: 'ref_phone',
        column: 'ref_phone',
        type: 'text',
        label: 'Référant Téléphone'
    }, {
        id: 'ref_mail',
        column: 'ref_mail',
        type: 'text',
        label: 'Référant Email'
    }, {
        id: 'contact_nom',
        column: 'contact_nom',
        type: 'text',
        label: 'Contact Nom'
    }, {
        id: 'contact_fonction',
        column: 'contact_fonction',
        type: 'text',
        label: 'Contact Fonction'
    }, {
        id: 'contact_phone',
        column: 'contact_phone',
        type: 'text',
        label: 'Contact Téléphone'
    }, {
        id: 'contact_mail',
        column: 'contact_mail',
        type: 'text',
        label: 'Contact Email'
    }, {
        id: 'couverture',
        column: 'couverture',
        type: 'lov',
        lovTable: 'lov_couverture',
        label: 'Couverture',
        readOnly: false
    }, {
        id: 'couverture_meta',
        column: 'couverture_meta',
        type: 'text',
        label: 'Couverture - Autre'
    }, {
        id: 'acces',
        column: 'acces',
        type: 'lov',
        lovTable: 'lov_acces',
        label: 'Accès',
        readOnly: false
    }, {
        id: 'acces_meta',
        column: 'acces_meta',
        type: 'text',
        label: 'Accès - Autre'
    }, {
        id: 'accueil_pmr',
        column: 'accueil_pmr',
        type: 'boolean',
        label: 'Accueil PMR'
    }, {
        id: 'pmr',
        column: 'pmr',
        type: 'lov',
        lovTable: 'lov_pmr',
        label: 'PMR',
        readOnly: false
    }, {
        id: 'pmr_meta',
        column: 'pmr_meta',
        type: 'text',
        label: 'PMR - Autre'
    }, {
        id: 'amenagement',
        column: 'amenagement',
        type: 'lov',
        lovTable: 'lov_amenagement',
        label: 'Aménagements',
        readOnly: false
    }, {
        id: 'amenagement_meta',
        column: 'amenagement_meta',
        type: 'text',
        label: 'Aménagements - Autre'
    }, {
        id: 'materiel',
        column: 'materiel',
        type: 'lov',
        lovTable: 'lov_materiel',
        label: 'Matériel',
        readOnly: false
    }, {
        id: 'materiel_meta',
        column: 'materiel_meta',
        type: 'text',
        label: 'Matériel - Autre'
    }, {
        id: 'plateforme',
        column: 'plateforme',
        type: 'boolean',
        label: 'Collaboration Plateforme'
    }, {
        id: 'plateforme_nom',
        column: 'plateforme_nom',
        type: 'text',
        label: 'Matériel - Autre'
    }]
}
