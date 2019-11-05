module.exports = {
    id: "asset",
    label: "Éléments de contenu",
    name: "asset",
    namePlural: "assets",
    icon: "todo.gif",
    titleField: "id_internal",

    fields: [{
        id: "key",
        label: "Clé",
        type: "text",
        width: 30,
        maxLength: 120,
        required: true,
        inMany: true
    }, {
        id: "description",
        label: "Groupe",
        type: "text",
        width: 100,
        maxLength: 250,
        required: true,
        inMany: true
    }, {
        id: "value",
        label: "Contenu",
        type: "textmultiline",
        width: 180,
        height: 11,
        required: true,
        inMany: true
    }, {
        id: "markdown",
        label: "Contenu Markdown",
        type: "boolean",
        required: false,
        inMany: false
    }],

    groups: [{
        id: "p1",
        type: "panel",
        label: "Meta",
        width: 100,
        fields: ["key", "markdown", "description"]
    }, {
        id: "p2",
        type: "panel",
        label: "Données",
        width: 100,
        fields: ["value"]
    }]

}
