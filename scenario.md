# 🥐 Odoo Tech Evening — Croissantage Website (Odoo 19)

## Sujet : Classement des Croissanteurs (participations)

---

## ✅ Todo (Préparation DB)

- [ ] Préparer la DB avec **> 50 croissantages**.
- [ ] Répartir les dates sur plusieurs semaines.
- [ ] Avoir plusieurs `croissanter_ids` par event (idéalement 2–3).
- [ ] Avoir des events en `state="done"`.

---

## 🎯 Objectif

### 1) Page "Leaderboard des Croissanteurs"

| Rang | Croissanteur | Participations |
| :--- | :----------- | :------------- |
| 1    | Florent      | 14             |
| 2    | Benjamin     | 11             |

**Fonctionnalités :**
* Génération de la table **côté serveur** via QWeb.
* Barre de recherche JS : masque dynamiquement les lignes qui ne correspondent pas au nom cherché (sans appel serveur).

### 2) Page "Soumettre un croissantage"

**Formulaire simple :**
> Nom : __________________  
> Victime : ______________  
> **[ SUBMIT ]**

**Règles :**
* Le croissanteur = l'utilisateur connecté.
* On crée un record en backend.

---

## 1. Controller HTTP (Calcul & Rendu)

C'est ici que se trouve le cœur du moteur : le contrôleur fait le calcul et envoie les données prêtes à être affichées au template.

```python
from odoo import http
from odoo.http import request

class CroissantageWebsite(http.Controller):

    @http.route('/croissantage', type='http', auth='public', website=True)
    def croissantage_page(self, **kwargs):
        # 1. Récupérer les événements terminés
        events = request.env['croissantage.event'].sudo().search([
            ('state', '=', 'done')
        ])
        
        # 2. Agréger les participations
        # Dictionnaire {partner_id: count}
        counts = {}
        for event in events:
            for partner in event.croissanter_ids:
                counts[partner] = counts.get(partner, 0) + 1
                
        # 3. Transformer en liste et trier (descendant)
        leaderboard = sorted(
            [{'partner': p, 'count': c} for p, c in counts.items()],
            key=lambda x: x['count'],
            reverse=True
        )

        # 4. Rendre le template avec les valeurs
        return request.render("croissantage.leaderboard_page", {
            'leaderboard': leaderboard,
        })
```

---

## 2. Page Website (Template QWeb)

### 2.a Bases
* Création d’une `website.page` (`id="leaderboard_page"`)
* Création d’un `website.menu`
* Héritage de `website.layout`

**Contenu avec la boucle QWeb (`t-foreach`) :**
```xml
<t t-call="website.layout">
    <div class="container mt-5">
        <h1>Hall of Croissants 🥐</h1>
        
        <input type="text" id="croissantageSearch" class="form-control mb-4" placeholder="Rechercher un croissanteur..."/>

        <table class="table table-striped" id="croissantageTable">
            <thead>
                <tr>
                    <th>Rang</th>
                    <th>Croissanteur</th>
                    <th>Participations</th>
                </tr>
            </thead>
            <tbody>
                <t t-foreach="leaderboard" t-as="row">
                    <tr class="croissanteur-row">
                        <td>
                            <span t-attf-class="badge #{
                                'text-bg-warning' if row_index == 0 else 
                                'text-bg-secondary' if row_index == 1 else 
                                'croissantage-badge-bronze' if row_index == 2 else 
                                'text-bg-light'}">
                                #<t t-out="row_index + 1"/>
                            </span>
                        </td>
                        <td class="croissanteur-name"><t t-out="row['partner'].name"/></td>
                        <td><t t-out="row['count']"/></td>
                    </tr>
                </t>
            </tbody>
        </table>
    </div>
</t>
```

---

## 3. JavaScript Vanilla — Le filtre dynamique

Puisque le tableau est généré côté serveur, on utilise un petit script JS très léger pour écouter l'input de recherche et masquer les lignes en CSS (`d-none`).

### 3.a Déclaration assets (`__manifest__.py`)
```python
'assets': {
    'web.assets_frontend': [
        'croissantage/static/src/js/croissantage_search.js',
        'croissantage/static/src/scss/croissantage.scss',
    ],
},
```

### 3.b Le script client
**Fichier :** `static/src/js/croissantage_search.js`

```javascript
/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CroissantageSearch = publicWidget.Widget.extend({
    selector: '#croissantageSearch',
    events: {
        'input': '_onSearchInput',
    },

    _onSearchInput: function (ev) {
        const searchTerm = ev.currentTarget.value.toLowerCase();
        const rows = document.querySelectorAll('.croissanteur-row');

        rows.forEach(row => {
            const nameCell = row.querySelector('.croissanteur-name');
            if (nameCell) {
                const name = nameCell.textContent.toLowerCase();
                // Bascule la classe Bootstrap "d-none" si le texte ne matche pas
                row.classList.toggle('d-none', !name.includes(searchTerm));
            }
        });
    },
});
```

---

## 4. SCSS Custom

**Fichier :** `static/src/scss/croissantage.scss`

Pour garder le côté stylé du top 3 :
```scss
.croissantage-badge-bronze {
    background-color: #cd7f32;
    color: white;
}
```

---

## 5. Page Submit

### 5.a Template

**Nouvelle `website.page` :**
```xml
<form method="post" action="/croissantage/submit">
    <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
    <input name="name" class="form-control mb-2" placeholder="Nom du croissantage" required="1"/>
    <input name="victime" class="form-control mb-2" placeholder="Victime" required="1"/>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### 5.b Route POST Protégée

```python
@http.route('/croissantage/submit',
            type='http',
            auth='user', # Protégé : utilisateur connecté requis
            methods=['POST'],
            website=True,
            csrf=True)
def croissantage_submit(self, **post):
    request.env['croissantage.event'].create({
        'name': post.get('name'),
        # Assigne le partenaire de l'utilisateur connecté
        'croissanter_ids': [(4, request.env.user.partner_id.id)],
    })
    return request.redirect('/croissantage')
```

---

## 🔁 Flow de la présentation

1. **Route HTTP (Contrôleur)** : L'ORM récupère, filtre, compte et trie les données.
2. **Template QWeb** : Utilisation de `t-foreach`, `t-out` et `t-attf-class` pour générer le tableau HTML.
3. **JS Widget (Client)** : Mise en place de l'input `keyup/input` pour cacher/afficher les `.croissanteur-row`.
4. **Formulaire Submit** : Explication de la méthode POST avec le token CSRF.
5. **Sécurité** : Différence fondamentale entre `auth='public'` (pour lire le classement) et `auth='user'` (pour soumettre un exploit).

---

## 🧠 Ce que ça démontre

* **Le pattern classique d'Odoo MVC** : Model (ORM) -> Controller (HTTP) -> View (QWeb).
* **QWeb Server-side** : Puissance de calcul et mise en page avant l'envoi au navigateur.
* **JS minimaliste** : Comment enrichir une page statique sans sur-ingénierie avec un `public.Widget`.
* **Sécurité des routes** : Gestion des droits et des formulaires protégés (CSRF).