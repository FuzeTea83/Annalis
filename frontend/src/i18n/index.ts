import { createI18n } from "vue-i18n";
import { french } from "./french";
import { english } from "./english";

const i18n = createI18n({
    legacy: false,
    locale: "fr-FR",
    fallbackLocale: "fr-FR",
    messages: {
        "fr-FR": french.messages,
        "en-US": english.messages
    } as Record<string, any>,
    datetimeFormats: {
        "fr-FR": french.datetimeFormats,
        "en-US": english.datetimeFormats
    } as Record<string, any>,
} as any);

export { i18n };