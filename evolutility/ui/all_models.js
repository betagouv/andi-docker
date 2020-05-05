/*
  Evolutility UI Models
  https://github.com/evoluteur/evolutility-ui-react
*/

import {
    prepModel,
    prepModelCollecs
} from '../utils/dico'

import user from './user_model'
import asset from './asset_model'
import accueil from './accueil_model'
import company from './company_model'
import jdb_psh from './jdb_psh_model'
import jdb_entreprise from './jdb_entreprise_model'


let models = {
    user: user,
    asset: asset,
    company: company,
    jdb_psh: jdb_psh,
    jdb_entreprise: jdb_entreprise,
    accueil: accueil,
}

const ms = Object.keys(models)
// need 2 passes for field map to be populated first, then collecs
ms.forEach(m => {
    models[m] = prepModel(models[m])
})
ms.forEach(m => {
    models[m] = prepModelCollecs(models, models[m])
})

export default models
