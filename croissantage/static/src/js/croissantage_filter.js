import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export class CroissantageInteraction extends Interaction {
    static selector = ".filter_croissantage";
    dynamicContent = {
        "#filter_name": {
            "t-on-input": this.onInputFilterName,
        },
    };

    setup() {
        
    }

    async onInputFilterName(ev) {
        const allLi = this.el.querySelectorAll("li[data-name]");
        const inputContent = ev.target.value.toLowerCase();

        allLi.forEach((li) => {
            const name = li.getAttribute("data-name").toLowerCase();
            if (name.includes(inputContent)) {
                li.classList.remove("d-none");
            } else {
                li.classList.add("d-none");
            }
        });
    }
}

registry.category("public.interactions").add("croissantage.CroissantageInteraction", CroissantageInteraction);