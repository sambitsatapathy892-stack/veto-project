import copy
import difflib
import re


PRODUCTS = {
    "Jio Fiber": {
        "aliases": ["jiofiber", "jio fiber broadband", "jio broadband", "jio wifi"],
        "score": 74,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "⚠️",
        "complaints": 38,
        "praises": 57,
        "bad_points": [
            "Support quality can vary a lot by area.",
            "Installation and issue resolution can feel slow in some locations.",
            "Service experience is not equally strong in every city or locality.",
        ],
        "good_points": [
            "Strong speed-to-price value in many areas.",
            "Useful bundled plans for OTT and home internet users.",
            "Generally fast enough for streaming, classes, and work-from-home use.",
        ],
        "voices": [
            "Speed is good when the line is stable, but support really depends on where you live.",
            "Works well for daily use, but downtime handling can be frustrating.",
            "Great value if your area has strong service quality.",
        ],
        "alt_name": "Airtel",
        "alt_score": 81,
        "alt_reason": "Often preferred for more consistent service quality and support experience in many areas.",
        "alt_good": [
            "Usually seen as a more stable broadband option.",
            "Support experience is often rated better than average.",
        ],
        "alt_bad": [
            "Pricing can feel slightly higher in some plans.",
        ],
        "product_links": [
            {"label": "Jio official site", "url": "https://www.jio.com/"},
        ],
        "review_links": [
            {"label": "MyJio Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.jio.myjio&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Airtel broadband", "url": "https://www.airtel.in/broadband/"},
        ],
        "sources": [
            {"label": "Jio official site", "url": "https://www.jio.com/"},
            {"label": "MyJio Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.jio.myjio&showAllReviews=true"},
            {"label": "Airtel broadband", "url": "https://www.airtel.in/broadband/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "boAt Airdopes": {
        "aliases": ["boat airdopes", "airdopes", "boat earbuds", "boat tws"],
        "score": 68,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "🎧",
        "complaints": 29,
        "praises": 49,
        "bad_points": [
            "Long-term durability can be inconsistent across models.",
            "Mic and call quality is not equally strong on every variant.",
            "Battery performance can reduce noticeably over time on some units.",
        ],
        "good_points": [
            "Very attractive pricing for budget wireless earbuds.",
            "Easy to buy and widely available.",
            "Looks modern and works fine for casual listening.",
        ],
        "voices": [
            "Good for the price, but not always something I would trust for long-term heavy use.",
            "Looks stylish and sounds decent enough for normal daily use.",
            "Worth it for budget buyers if expectations are realistic.",
        ],
        "alt_name": "OnePlus",
        "alt_score": 79,
        "alt_reason": "Usually preferred when the buyer wants a slightly more reliable overall experience.",
        "alt_good": [
            "Often seen as more balanced in sound and build.",
            "Better fit for buyers who want fewer compromises.",
        ],
        "alt_bad": [
            "Can cost more than budget boAt options.",
        ],
        "product_links": [
            {"label": "boAt Airdopes collection", "url": "https://www.boat-lifestyle.com/collections/airdopes"},
            {"label": "boAt official site", "url": "https://www.boat-lifestyle.com/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "OnePlus audio", "url": "https://www.oneplus.in/store/audio"},
        ],
        "sources": [
            {"label": "boAt Airdopes collection", "url": "https://www.boat-lifestyle.com/collections/airdopes"},
            {"label": "boAt support", "url": "https://support.boat-lifestyle.com/"},
            {"label": "OnePlus audio", "url": "https://www.oneplus.in/store/audio"},
        ],
        "amazon_search_term": "boAt Airdopes",
        "flipkart_search_term": "boAt Airdopes",
    },

    "Zomato": {
        "aliases": ["zomato app", "zomato delivery", "zomato food"],
        "score": 72,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "🍔",
        "complaints": 41,
        "praises": 63,
        "bad_points": [
            "Refund and support handling can feel inconsistent.",
            "Delivery fees and surge pricing can frustrate users.",
            "Order experience can vary heavily by city and restaurant.",
        ],
        "good_points": [
            "Huge restaurant network and easy app experience.",
            "Strong convenience for fast food ordering.",
            "Useful offers and filters in many cities.",
        ],
        "voices": [
            "Convenient, but support becomes the problem when something goes wrong.",
            "Great app when the order goes right, stressful when it doesn’t.",
            "Still one of the easiest food apps to use.",
        ],
        "alt_name": "Swiggy",
        "alt_score": 77,
        "alt_reason": "Often chosen as the closest strong alternative for delivery experience and restaurant coverage.",
        "alt_good": [
            "Strong delivery ecosystem and broad restaurant presence.",
            "Good backup option if Zomato feels unreliable in a specific area.",
        ],
        "alt_bad": [
            "Pricing and fees can still be annoying.",
        ],
        "product_links": [
            {"label": "Zomato official site", "url": "https://www.zomato.com/"},
        ],
        "review_links": [
            {"label": "Zomato Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.application.zomato&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Swiggy official site", "url": "https://www.swiggy.com/"},
        ],
        "sources": [
            {"label": "Zomato official site", "url": "https://www.zomato.com/"},
            {"label": "Zomato Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.application.zomato&showAllReviews=true"},
            {"label": "Swiggy official site", "url": "https://www.swiggy.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "BYJU'S": {
        "aliases": ["byjus", "byju's app", "byjus learning app", "byju"],
        "score": 34,
        "verdict": "AVOID",
        "color": "red",
        "emoji": "🚫",
        "complaints": 54,
        "praises": 21,
        "bad_points": [
            "Strong trust concerns around sales pressure and aggressive follow-up.",
            "Many users feel product value did not justify the cost.",
            "Brand trust has taken visible damage over time.",
        ],
        "good_points": [
            "Well-known brand recall in edtech.",
            "Can still feel useful for some structured learners.",
        ],
        "voices": [
            "The product may work for some students, but trust is the bigger issue here.",
            "Too many people complain about the selling process.",
            "The name is big, but the confidence level is not.",
        ],
        "alt_name": "Khan Academy",
        "alt_score": 86,
        "alt_reason": "A much safer trust-first alternative for learning support.",
        "alt_good": [
            "Widely trusted and easy to access.",
            "Focuses more on learning than pressure selling.",
        ],
        "alt_bad": [
            "May feel less guided for users wanting a highly managed system.",
        ],
        "product_links": [
            {"label": "BYJU'S official site", "url": "https://byjus.com/"},
        ],
        "review_links": [
            {"label": "BYJU'S Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.byjus.thelearningapp&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Khan Academy", "url": "https://www.khanacademy.org/"},
        ],
        "sources": [
            {"label": "BYJU'S official site", "url": "https://byjus.com/"},
            {"label": "BYJU'S Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.byjus.thelearningapp&showAllReviews=true"},
            {"label": "Khan Academy", "url": "https://www.khanacademy.org/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "OYO Rooms": {
        "aliases": ["oyo", "oyo hotel", "oyo rooms hotel", "oyo stay"],
        "score": 46,
        "verdict": "WAIT",
        "color": "orange",
        "emoji": "🏨",
        "complaints": 52,
        "praises": 28,
        "bad_points": [
            "Actual hotel quality can differ sharply from listing expectations.",
            "Check-in disputes and property mismatch are recurring worries.",
            "User trust depends heavily on the exact property, not just the app brand.",
        ],
        "good_points": [
            "Widely available and often budget-friendly.",
            "Can still be useful for short budget stays when chosen carefully.",
        ],
        "voices": [
            "You are not booking OYO, you are really booking the specific property.",
            "Some stays are fine, but inconsistency is the risk.",
            "Use only after checking recent property-level feedback carefully.",
        ],
        "alt_name": "MakeMyTrip",
        "alt_score": 73,
        "alt_reason": "Often preferred when users want broader filtering and stronger booking confidence.",
        "alt_good": [
            "Broader hotel discovery and comparison experience.",
            "Usually better for cross-checking before booking.",
        ],
        "alt_bad": [
            "Pricing may not always be the lowest.",
        ],
        "product_links": [
            {"label": "OYO official site", "url": "https://www.oyorooms.com/"},
        ],
        "review_links": [
            {"label": "OYO Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.oyo.consumer&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "MakeMyTrip", "url": "https://www.makemytrip.com/"},
        ],
        "sources": [
            {"label": "OYO official site", "url": "https://www.oyorooms.com/"},
            {"label": "OYO Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.oyo.consumer&showAllReviews=true"},
            {"label": "MakeMyTrip", "url": "https://www.makemytrip.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Redmi": {
        "aliases": ["redmi phone", "mi phone", "xiaomi phone", "redmi mobile"],
        "score": 64,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "📱",
        "complaints": 35,
        "praises": 51,
        "bad_points": [
            "Software experience and long-term smoothness can divide users.",
            "Ads and UI experience have historically frustrated some buyers.",
            "After-sales confidence is not equally strong everywhere.",
        ],
        "good_points": [
            "Very strong hardware value for the price segment.",
            "Popular choice for budget-conscious buyers.",
            "Wide range of options across price points.",
        ],
        "voices": [
            "Great specs for money, but software trade-offs are real.",
            "Good value buy if you care more about hardware than premium feel.",
            "Worth considering, but not blindly.",
        ],
        "alt_name": "OnePlus",
        "alt_score": 78,
        "alt_reason": "Often preferred by users who want a more refined overall smartphone experience.",
        "alt_good": [
            "Usually feels cleaner and more polished overall.",
            "Better fit for users wanting a more premium experience.",
        ],
        "alt_bad": [
            "Higher price in many segments.",
        ],
        "product_links": [
            {"label": "Xiaomi India", "url": "https://www.mi.com/in/"},
            {"label": "Mi Store", "url": "https://www.mi.com/in/store/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
        ],
        "sources": [
            {"label": "Xiaomi India", "url": "https://www.mi.com/in/"},
            {"label": "Mi Store", "url": "https://www.mi.com/in/store/"},
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
        ],
        "amazon_search_term": "Redmi smartphone",
        "flipkart_search_term": "Redmi smartphone",
    },

    "Airtel": {
        "aliases": ["airtel broadband", "airtel xstream", "airtel fiber", "airtel sim"],
        "score": 77,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 27,
        "praises": 58,
        "bad_points": [
            "Plan pricing can feel high in some use cases.",
            "Service quality still depends on city and locality.",
        ],
        "good_points": [
            "Strong overall brand trust for connectivity.",
            "Often rated better than average for broadband stability.",
            "Useful all-in-one ecosystem for many users.",
        ],
        "voices": [
            "Usually more dependable than many people expect.",
            "A safer broadband pick in many areas if the plan fits your budget.",
            "Good option when support reliability matters.",
        ],
        "alt_name": "Jio Fiber",
        "alt_score": 74,
        "alt_reason": "Still a strong price-value alternative depending on your area.",
        "alt_good": [
            "Often better on value and bundled plans.",
            "Good competitor if your locality has strong Jio service.",
        ],
        "alt_bad": [
            "Support consistency can vary more by area.",
        ],
        "product_links": [
            {"label": "Airtel official site", "url": "https://www.airtel.in/"},
            {"label": "Airtel broadband", "url": "https://www.airtel.in/broadband/"},
        ],
        "review_links": [
            {"label": "Airtel Thanks Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.myairtelapp&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Jio official site", "url": "https://www.jio.com/"},
        ],
        "sources": [
            {"label": "Airtel official site", "url": "https://www.airtel.in/"},
            {"label": "Airtel Thanks Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.myairtelapp&showAllReviews=true"},
            {"label": "Jio official site", "url": "https://www.jio.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Ola": {
        "aliases": ["ola cabs", "ola app", "ola taxi", "ola cab"],
        "score": 58,
        "verdict": "WAIT",
        "color": "orange",
        "emoji": "🚕",
        "complaints": 44,
        "praises": 34,
        "bad_points": [
            "Ride consistency and pricing trust can be unstable.",
            "Cancellation and service experience can frustrate users.",
            "User experience can vary a lot by driver and city.",
        ],
        "good_points": [
            "Large brand presence and easy app familiarity.",
            "Useful when availability is good in your location.",
        ],
        "voices": [
            "It works when it works, but confidence is not always high.",
            "A backup option, not always a blind-trust option.",
            "Can still be useful depending on city and timing.",
        ],
        "alt_name": "Uber",
        "alt_score": 76,
        "alt_reason": "Often preferred when users want a more globally trusted ride-booking experience.",
        "alt_good": [
            "Stronger familiarity and consistency for many users.",
            "Often chosen as the more dependable ride alternative.",
        ],
        "alt_bad": [
            "Pricing can still spike depending on demand.",
        ],
        "product_links": [
            {"label": "Ola official site", "url": "https://www.olacabs.com/"},
        ],
        "review_links": [
            {"label": "Ola Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.olacabs.customer&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Uber India", "url": "https://www.uber.com/in/en/"},
        ],
        "sources": [
            {"label": "Ola official site", "url": "https://www.olacabs.com/"},
            {"label": "Ola Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.olacabs.customer&showAllReviews=true"},
            {"label": "Uber India", "url": "https://www.uber.com/in/en/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Swiggy": {
        "aliases": ["swiggy app", "swiggy food", "swiggy delivery"],
        "score": 76,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 32,
        "praises": 61,
        "bad_points": [
            "Fees and charges can still irritate frequent users.",
            "Support quality is not perfect when orders go wrong.",
        ],
        "good_points": [
            "Very strong convenience and app familiarity.",
            "Broad restaurant coverage in many cities.",
            "Often preferred for dependable ordering flow.",
        ],
        "voices": [
            "Usually one of the safer food delivery choices.",
            "Still not perfect, but easier to trust than many weaker alternatives.",
            "Convenient and fast for regular users.",
        ],
        "alt_name": "Zomato",
        "alt_score": 72,
        "alt_reason": "A strong parallel option depending on offers and restaurant availability.",
        "alt_good": [
            "Huge city coverage and strong restaurant listings.",
            "Still one of the top alternatives in food delivery.",
        ],
        "alt_bad": [
            "Support and refunds can still be inconsistent.",
        ],
        "product_links": [
            {"label": "Swiggy official site", "url": "https://www.swiggy.com/"},
        ],
        "review_links": [
            {"label": "Swiggy Google Play reviews", "url": "https://play.google.com/store/apps/details?id=in.swiggy.android&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Zomato official site", "url": "https://www.zomato.com/"},
        ],
        "sources": [
            {"label": "Swiggy official site", "url": "https://www.swiggy.com/"},
            {"label": "Swiggy Google Play reviews", "url": "https://play.google.com/store/apps/details?id=in.swiggy.android&showAllReviews=true"},
            {"label": "Zomato official site", "url": "https://www.zomato.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "OnePlus": {
        "aliases": ["one plus", "oneplus phone", "oneplus mobile"],
        "score": 79,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 26,
        "praises": 55,
        "bad_points": [
            "Pricing has become less budget-friendly over time.",
            "Some users feel the old brand identity was stronger than now.",
        ],
        "good_points": [
            "Generally more refined overall than many mid-range competitors.",
            "Cleaner premium feel for buyers wanting less compromise.",
            "Stronger brand pull for performance-focused users.",
        ],
        "voices": [
            "A more confident buy than many value brands if budget allows.",
            "Feels more polished overall for daily use.",
            "Good option when you want balance, not just raw specs.",
        ],
        "alt_name": "Samsung",
        "alt_score": 82,
        "alt_reason": "Often preferred by buyers who want a mature ecosystem and stronger mainstream trust.",
        "alt_good": [
            "Strong brand trust and wide service presence.",
            "Great option for users wanting reliability and ecosystem depth.",
        ],
        "alt_bad": [
            "Some models can feel expensive for the specs offered.",
        ],
        "product_links": [
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
            {"label": "OnePlus store", "url": "https://www.oneplus.in/store"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
        ],
        "sources": [
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
            {"label": "OnePlus store", "url": "https://www.oneplus.in/store"},
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
        ],
        "amazon_search_term": "OnePlus smartphone",
        "flipkart_search_term": "OnePlus smartphone",
    },

    "Samsung": {
        "aliases": ["samsung phone", "samsung mobile", "galaxy phone", "samsung smartphone"],
        "score": 82,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 24,
        "praises": 62,
        "bad_points": [
            "Some models feel expensive for the raw specs offered.",
            "Budget and mid-range models can vary a lot in value.",
        ],
        "good_points": [
            "Very strong mainstream trust and brand reliability.",
            "Good service network and ecosystem familiarity.",
            "Safer choice for buyers wanting consistency over hype.",
        ],
        "voices": [
            "Usually a safer buy if you want fewer surprises.",
            "More trust-driven than spec-driven for many people.",
            "Good fit for long-term mainstream users.",
        ],
        "alt_name": "OnePlus",
        "alt_score": 79,
        "alt_reason": "Often preferred by buyers who want a more performance-premium feel.",
        "alt_good": [
            "Feels more enthusiast-oriented in many segments.",
            "Strong option for users who value smoothness and polish.",
        ],
        "alt_bad": [
            "Not always as broad or mainstream in support trust.",
        ],
        "product_links": [
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
        ],
        "sources": [
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
            {"label": "Samsung India", "url": "https://www.samsung.com/in/"},
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
        ],
        "amazon_search_term": "Samsung smartphone",
        "flipkart_search_term": "Samsung smartphone",
    },

    "Uber": {
        "aliases": ["uber cab", "uber taxi", "uber app", "uber rides"],
        "score": 76,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 28,
        "praises": 53,
        "bad_points": [
            "Surge pricing can still be painful at peak times.",
            "Ride experience still depends on driver and city.",
        ],
        "good_points": [
            "Widely trusted ride-booking option.",
            "Generally stronger reliability perception than weaker ride apps.",
            "Good familiarity and ease of use.",
        ],
        "voices": [
            "Usually the more dependable ride app if available well in your city.",
            "Still not perfect, but easier to trust for many users.",
            "Good default option when you want less uncertainty.",
        ],
        "alt_name": "Ola",
        "alt_score": 58,
        "alt_reason": "Useful backup option depending on city availability and pricing.",
        "alt_good": [
            "Can help when Uber availability is weak.",
            "Good as a secondary ride app on your phone.",
        ],
        "alt_bad": [
            "Ride consistency and trust can feel lower.",
        ],
        "product_links": [
            {"label": "Uber India", "url": "https://www.uber.com/in/en/"},
        ],
        "review_links": [
            {"label": "Uber Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.ubercab&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Ola official site", "url": "https://www.olacabs.com/"},
        ],
        "sources": [
            {"label": "Uber India", "url": "https://www.uber.com/in/en/"},
            {"label": "Uber Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.ubercab&showAllReviews=true"},
            {"label": "Ola official site", "url": "https://www.olacabs.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Realme": {
        "aliases": ["realme phone", "realme mobile", "real me", "realme smartphone"],
        "score": 69,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "📱",
        "complaints": 31,
        "praises": 48,
        "bad_points": [
            "Software experience may not feel premium to every buyer.",
            "Model-to-model consistency can vary a lot.",
        ],
        "good_points": [
            "Strong value in the budget and mid-range segment.",
            "Often attractive for spec-focused buyers.",
            "Popular among buyers wanting modern looks at lower cost.",
        ],
        "voices": [
            "Good value, but software polish can decide whether you like it or not.",
            "A sensible option if specs matter more than brand prestige.",
            "Worth considering in the right budget band.",
        ],
        "alt_name": "Redmi",
        "alt_score": 64,
        "alt_reason": "Another strong value-first smartphone competitor in the same buying zone.",
        "alt_good": [
            "Competitive pricing and wide range of options.",
            "Useful comparison point for budget buyers.",
        ],
        "alt_bad": [
            "Software trade-offs are still real there too.",
        ],
        "product_links": [
            {"label": "Realme India", "url": "https://www.realme.com/in/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "Xiaomi India", "url": "https://www.mi.com/in/"},
        ],
        "sources": [
            {"label": "Realme India", "url": "https://www.realme.com/in/"},
            {"label": "Xiaomi India", "url": "https://www.mi.com/in/"},
            {"label": "OnePlus official site", "url": "https://www.oneplus.in/"},
        ],
        "amazon_search_term": "Realme smartphone",
        "flipkart_search_term": "Realme smartphone",
    },

    "Vivo": {
        "aliases": ["vivo phone", "vivo mobile", "vivo smartphone"],
        "score": 63,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "📱",
        "complaints": 33,
        "praises": 42,
        "bad_points": [
            "Value-for-money can feel weaker compared to some aggressive competitors.",
            "Software and brand preference can be polarizing.",
        ],
        "good_points": [
            "Strong offline visibility and brand familiarity.",
            "Some buyers like the design and camera-focused positioning.",
            "Easy brand recall in the Indian market.",
        ],
        "voices": [
            "Works for many mainstream buyers, but comparison shopping is important here.",
            "Good enough in some cases, but not always the best value pick.",
            "Design appeal helps, but specs comparison still matters.",
        ],
        "alt_name": "Samsung",
        "alt_score": 82,
        "alt_reason": "Often preferred by buyers wanting higher long-term confidence and broader trust.",
        "alt_good": [
            "Usually feels safer as a mainstream long-term choice.",
            "Stronger brand trust for many buyers.",
        ],
        "alt_bad": [
            "Can cost more in equivalent segments.",
        ],
        "product_links": [
            {"label": "Vivo India", "url": "https://www.vivo.com/in/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
        ],
        "sources": [
            {"label": "Vivo India", "url": "https://www.vivo.com/in/"},
            {"label": "Samsung smartphones", "url": "https://www.samsung.com/in/smartphones/"},
        ],
        "amazon_search_term": "Vivo smartphone",
        "flipkart_search_term": "Vivo smartphone",
    },

    "Oppo": {
        "aliases": ["oppo phone", "oppo mobile", "oppo smartphone"],
        "score": 61,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "📱",
        "complaints": 32,
        "praises": 39,
        "bad_points": [
            "Pricing can feel high relative to competition in some segments.",
            "Many buyers still compare it critically on value.",
        ],
        "good_points": [
            "Strong offline presence and easy brand visibility.",
            "Design and camera positioning appeal to many mainstream buyers.",
        ],
        "voices": [
            "Can work fine, but it rarely feels like an automatic best-value choice.",
            "A compare-first phone brand, not a blind buy.",
            "Brand visibility is strong, but comparison still matters a lot.",
        ],
        "alt_name": "Realme",
        "alt_score": 69,
        "alt_reason": "Often considered when the buyer wants stronger value orientation.",
        "alt_good": [
            "Usually more value-focused in comparable ranges.",
            "Good alternative if budget efficiency matters more.",
        ],
        "alt_bad": [
            "Software polish may still divide users.",
        ],
        "product_links": [
            {"label": "OPPO India", "url": "https://www.oppo.com/in/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "Realme India", "url": "https://www.realme.com/in/"},
        ],
        "sources": [
            {"label": "OPPO India", "url": "https://www.oppo.com/in/"},
            {"label": "Realme India", "url": "https://www.realme.com/in/"},
        ],
        "amazon_search_term": "Oppo smartphone",
        "flipkart_search_term": "Oppo smartphone",
    },

    "MakeMyTrip": {
        "aliases": ["mmt", "makemy trip", "make my trip", "makemytrip app", "travel booking app"],
        "score": 73,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "✈️",
        "complaints": 30,
        "praises": 50,
        "bad_points": [
            "Refunds and changes can still become stressful in edge cases.",
            "Travel pricing and booking confidence depend on the exact listing and vendor.",
        ],
        "good_points": [
            "Strong travel discovery and comparison experience.",
            "Useful for flights, hotels, and broader planning.",
            "Often preferred for multi-option travel booking.",
        ],
        "voices": [
            "Good for comparing options, but verify final details carefully.",
            "Useful travel platform, especially when you want everything in one place.",
            "Convenient, but still needs smart checking before payment.",
        ],
        "alt_name": "Direct hotel or airline booking",
        "alt_score": 78,
        "alt_reason": "Sometimes safer when the booking is important and you want direct accountability.",
        "alt_good": [
            "Can reduce platform-level confusion in important bookings.",
            "More direct control in some situations.",
        ],
        "alt_bad": [
            "Less convenient for broad comparison.",
        ],
        "product_links": [
            {"label": "MakeMyTrip", "url": "https://www.makemytrip.com/"},
        ],
        "review_links": [
            {"label": "MakeMyTrip Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.makemytrip&showAllReviews=true"},
        ],
        "alt_links": [],
        "sources": [
            {"label": "MakeMyTrip", "url": "https://www.makemytrip.com/"},
            {"label": "MakeMyTrip Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.makemytrip&showAllReviews=true"},
            {"label": "OYO official site", "url": "https://www.oyorooms.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Urban Company": {
        "aliases": ["urban company app", "urban clap", "urbanclap", "home services app"],
        "score": 75,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 24,
        "praises": 54,
        "bad_points": [
            "Service quality can still depend on the assigned professional.",
            "Pricing can feel high for some categories.",
        ],
        "good_points": [
            "Strong convenience for home services.",
            "Useful discovery and booking system for urban users.",
            "Often easier than finding random local providers blindly.",
        ],
        "voices": [
            "A helpful service app when you want convenience and structure.",
            "Usually better than randomly searching for home service people online.",
            "Good if trust and ease matter more than cheapest price.",
        ],
        "alt_name": "Local verified provider",
        "alt_score": 68,
        "alt_reason": "Sometimes better if you already know a trusted local professional.",
        "alt_good": [
            "Can be cheaper in some cases.",
            "Good when personal trust already exists.",
        ],
        "alt_bad": [
            "Less standardized experience.",
        ],
        "product_links": [
            {"label": "Urban Company", "url": "https://www.urbancompany.com/"},
        ],
        "review_links": [],
        "alt_links": [],
        "sources": [
            {"label": "Urban Company", "url": "https://www.urbancompany.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "PolicyBazaar": {
        "aliases": ["policy bazaar", "policybazaar app", "insurance compare app", "insurance comparison site"],
        "score": 66,
        "verdict": "BUY WITH CAUTION",
        "color": "orange",
        "emoji": "🛡️",
        "complaints": 31,
        "praises": 43,
        "bad_points": [
            "Follow-up and sales contact can feel aggressive to some users.",
            "Insurance products still need careful manual verification.",
        ],
        "good_points": [
            "Useful for comparing insurance options in one place.",
            "Convenient for initial discovery and pricing checks.",
            "Strong brand recall in the insurance comparison category.",
        ],
        "voices": [
            "Helpful for comparing, but never buy without reading the policy properly.",
            "Good discovery layer, not a substitute for understanding the product.",
            "Convenient, but you still need to verify details yourself.",
        ],
        "alt_name": "Direct insurer website",
        "alt_score": 74,
        "alt_reason": "Sometimes safer if you already know the insurer you want and need direct clarity.",
        "alt_good": [
            "Less middle-layer confusion in some cases.",
            "More direct product verification.",
        ],
        "alt_bad": [
            "Comparison becomes slower and more manual.",
        ],
        "product_links": [
            {"label": "PolicyBazaar", "url": "https://www.policybazaar.com/"},
        ],
        "review_links": [],
        "alt_links": [],
        "sources": [
            {"label": "PolicyBazaar", "url": "https://www.policybazaar.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Myntra": {
        "aliases": ["myntra app", "myntra fashion", "fashion shopping app"],
        "score": 74,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 24,
        "praises": 52,
        "bad_points": [
            "Returns and delivery experience can still vary by item and seller.",
            "Discounts can sometimes create confusion on final value perception.",
        ],
        "good_points": [
            "Strong fashion-focused shopping experience.",
            "Good brand familiarity and broad catalog appeal.",
            "Easy for browsing, filtering, and style discovery.",
        ],
        "voices": [
            "One of the easiest fashion apps to browse comfortably.",
            "Useful if you like variety and style-first shopping.",
            "Good for fashion discovery, but still compare quality and return rules.",
        ],
        "alt_name": "Nykaa",
        "alt_score": 71,
        "alt_reason": "Useful alternative when the buyer is more focused on beauty, lifestyle, or category-specific shopping.",
        "alt_good": [
            "Strong niche trust in beauty and lifestyle.",
            "Good parallel shopping option depending on category.",
        ],
        "alt_bad": [
            "Not as broad in fashion-first use cases.",
        ],
        "product_links": [
            {"label": "Myntra", "url": "https://www.myntra.com/"},
        ],
        "review_links": [
            {"label": "Myntra Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.myntra.android&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Nykaa", "url": "https://www.nykaa.com/"},
        ],
        "sources": [
            {"label": "Myntra", "url": "https://www.myntra.com/"},
            {"label": "Myntra Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.myntra.android&showAllReviews=true"},
            {"label": "Nykaa", "url": "https://www.nykaa.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Nykaa": {
        "aliases": ["nykaa app", "nykaa beauty", "beauty shopping app"],
        "score": 71,
        "verdict": "BUY",
        "color": "green",
        "emoji": "✅",
        "complaints": 23,
        "praises": 49,
        "bad_points": [
            "Delivery and order experience can still vary across sellers and items.",
            "Beauty buying still needs product-level checking, not just platform trust.",
        ],
        "good_points": [
            "Strong category trust in beauty and personal care.",
            "Useful app experience for beauty-first buyers.",
            "Good catalog strength in its core niche.",
        ],
        "voices": [
            "A comfortable platform for beauty shopping if you already know what you want.",
            "Better category focus than general marketplaces in some beauty use cases.",
            "Still verify product and seller details before buying.",
        ],
        "alt_name": "Myntra",
        "alt_score": 74,
        "alt_reason": "Useful broader lifestyle alternative when shopping needs move beyond beauty.",
        "alt_good": [
            "Broader shopping ecosystem for style and lifestyle discovery.",
            "Good parallel option depending on category.",
        ],
        "alt_bad": [
            "Less niche beauty-focused than Nykaa.",
        ],
        "product_links": [
            {"label": "Nykaa", "url": "https://www.nykaa.com/"},
        ],
        "review_links": [
            {"label": "Nykaa Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.fsn.nykaa&showAllReviews=true"},
        ],
        "alt_links": [
            {"label": "Myntra", "url": "https://www.myntra.com/"},
        ],
        "sources": [
            {"label": "Nykaa", "url": "https://www.nykaa.com/"},
            {"label": "Nykaa Google Play reviews", "url": "https://play.google.com/store/apps/details?id=com.fsn.nykaa&showAllReviews=true"},
            {"label": "Myntra", "url": "https://www.myntra.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },

    "Meesho": {
        "aliases": ["meesho app", "meesho shopping", "reseller shopping app"],
        "score": 59,
        "verdict": "WAIT",
        "color": "orange",
        "emoji": "🛍️",
        "complaints": 38,
        "praises": 36,
        "bad_points": [
            "Product quality consistency can be uncertain in some listings.",
            "Trust depends heavily on the exact item and seller.",
            "Low-price attraction can sometimes hide quality risk.",
        ],
        "good_points": [
            "Very attractive pricing for budget buyers.",
            "Useful for low-cost discovery in some categories.",
            "Strong mass-market familiarity.",
        ],
        "voices": [
            "Good for cheap finds, but you really need to check carefully.",
            "Price is the attraction, quality confidence is the question.",
            "Best used with realistic expectations.",
        ],
        "alt_name": "Myntra",
        "alt_score": 74,
        "alt_reason": "Often safer when the buyer wants stronger shopping confidence over lowest price.",
        "alt_good": [
            "Better trust perception for a more polished shopping experience.",
            "Useful when quality confidence matters more than extreme low pricing.",
        ],
        "alt_bad": [
            "Usually not as cheap.",
        ],
        "product_links": [
            {"label": "Meesho", "url": "https://www.meesho.com/"},
        ],
        "review_links": [],
        "alt_links": [
            {"label": "Myntra", "url": "https://www.myntra.com/"},
        ],
        "sources": [
            {"label": "Meesho", "url": "https://www.meesho.com/"},
            {"label": "Myntra", "url": "https://www.myntra.com/"},
        ],
        "amazon_search_term": "",
        "flipkart_search_term": "",
    },
}


def _normalize(text):
    text = str(text).lower().strip()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _with_name(canonical_name):
    data = copy.deepcopy(PRODUCTS[canonical_name])
    data["name"] = canonical_name
    return data


def get_product_info(name):
    if not name:
        return None

    query = _normalize(name)

    for canonical_name, data in PRODUCTS.items():
        candidates = [canonical_name] + data.get("aliases", [])
        for item in candidates:
            if query == _normalize(item):
                return _with_name(canonical_name)

    for canonical_name, data in PRODUCTS.items():
        candidates = [canonical_name] + data.get("aliases", [])
        for item in candidates:
            item_norm = _normalize(item)
            if query in item_norm or item_norm in query:
                return _with_name(canonical_name)

    query_tokens = set(query.split())
    best_name = None
    best_score = 0

    for canonical_name, data in PRODUCTS.items():
        candidates = [canonical_name] + data.get("aliases", [])
        for item in candidates:
            item_tokens = set(_normalize(item).split())
            overlap = len(query_tokens & item_tokens)
            if overlap > best_score:
                best_score = overlap
                best_name = canonical_name

    if best_name and best_score > 0:
        return _with_name(best_name)

    all_names = []
    alias_to_name = {}

    for canonical_name, data in PRODUCTS.items():
        candidates = [canonical_name] + data.get("aliases", [])
        for item in candidates:
            norm_item = _normalize(item)
            all_names.append(norm_item)
            alias_to_name[norm_item] = canonical_name

    matches = difflib.get_close_matches(query, all_names, n=1, cutoff=0.6)
    if matches:
        return _with_name(alias_to_name[matches[0]])

    return None