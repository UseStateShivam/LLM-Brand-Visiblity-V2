from llm_brand_visiblity_v2.schemas import ContextEnum, TypeEnum, IntentEnum

templates = {
    TypeEnum.BRANDED: {
        IntentEnum.BUYING: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.COMPARISON: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        }
    },
    TypeEnum.UNBRANDED: {
        IntentEnum.BUYING: {
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.COMPARISON: {
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        }
    },
    TypeEnum.COMPETITOR: {
        IntentEnum.BUYING: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.INFORMATIONAL: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        },
        IntentEnum.COMPARISON: {
            ContextEnum.BRANDLEVEL: [],
            ContextEnum.PRODUCTLEVEL: [],
            ContextEnum.SERVICELEVEL: []
        }
    }
}