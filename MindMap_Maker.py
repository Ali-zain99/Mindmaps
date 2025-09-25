import zlib
import requests

# ---------- PlantUML encoding ----------
def encode6bit(b: int) -> str:
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return "-"
    if b == 1:
        return "_"
    return "?"

def append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        encode6bit(c1 & 0x3F)
        + encode6bit(c2 & 0x3F)
        + encode6bit(c3 & 0x3F)
        + encode6bit(c4 & 0x3F)
    )

def encode64(data: bytes) -> str:
    res = ""
    i = 0
    length = len(data)
    while i < length:
        if i + 2 == length:
            res += append3bytes(data[i], data[i + 1], 0)
        elif i + 1 == length:
            res += append3bytes(data[i], 0, 0)
        else:
            res += append3bytes(data[i], data[i + 1], data[i + 2])
        i += 3
    return res

def plantuml_encode(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"))[2:-4]  # strip zlib headers
    return encode64(compressed)

def generate_mindmap(uml_code: str, output_file: str = "mindmap.png"):
    encoded = plantuml_encode(uml_code)
    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(resp.content)
        print(f"[ok] Mind map saved to {output_file}")
    else:
        print(f"[error] PlantUML server {resp.status_code}: {resp.text[:200]}")

# ---------- Convert your outline into PlantUML ----------
uml_code = """

@startmindmap
* 340B Price Guide
** Home - 340B Price Guide (/) [[screenshots\35eceb47db2ee92eb53c9b97c1865c14.png]]
*** Link (Home)
*** Link (Search)
**** https://www.340bpriceguide.net/340b-search (/340b-search)
*** Link (Articles)
**** https://www.340bpriceguide.net/articles-news (/articles-news)
*** Link (About)
**** https://www.340bpriceguide.net/about-us (/about-us)
*** Link (Contact)
**** https://www.340bpriceguide.net/contact-us (/contact-us)
*** Link (Forgot your password?)
**** https://www.340bpriceguide.net/client-login?view=reset (/client-login)
*** Link (Forgot your username?)
**** https://www.340bpriceguide.net/client-login?view=remind (/client-login)
*** Link (Create an account)
**** https://www.340bpriceguide.net/client-login?view=registration (/client-login)
*** Link (WHAT IS 340B?)
**** https://www.340bpriceguide.net/articles-news/50-what-is-340b (/articles-news/50-what-is-340b)
*** Link (WEEKLY PRODUCT SHORTAGES)
**** https://www.340bpriceguide.net/articles-news/126-weekly-product-shortages (/articles-news/126-weekly-product-shortages)
*** Link (Home)
**** https://www.340bpriceguide.net/index.php (/index.php)
*** Link (About Us)
**** https://www.340bpriceguide.net/index.php/about-us (/index.php/about-us)
*** Link (Articles & News)
**** Articles and News - 340B Price Guide (/index.php/articles-news) [[screenshots\60196bcdc6b39043c1482eb75852ac8d.png]]
***** Link (Home)
***** Link (Search)
***** Link (Articles)
***** Link (About)
***** Link (Contact)
***** Link (Forgot your password?)
***** Link (Forgot your username?)
***** Link (Create an account)
***** Link (WEEKLY PRODUCT SHORTAGES)
***** Link (Print)
****** https://www.340bpriceguide.net/articles-news/126-weekly-product-shortages?tmpl=component&print=1&layout=default (/articles-news/126-weekly-product-shortages)
***** Link (Email)
****** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=48f36ca13f26e4d5730c8eb5ff22f26733881327 (/component/mailto/)
***** Link (READ MORE ...)
***** Link (THE FREESTYLE LIBRE 2 AND FREESTYLE LIBRE 3 SENSORS WILL BE DISCONTINUED IN SEPTEMBER)
****** https://www.340bpriceguide.net/articles-news/141-the-freestyle-libre-2-and-freestyle-libre-3-sensors-will-be-discontinued-in-september (/articles-news/141-the-freestyle-libre-2-and-freestyle-libre-3-sensors-will-be-discontinued-in-september)
***** Link (Print)
****** https://www.340bpriceguide.net/articles-news/141-the-freestyle-libre-2-and-freestyle-libre-3-sensors-will-be-discontinued-in-september?tmpl=component&print=1&layout=default (/articles-news/141-the-freestyle-libre-2-and-freestyle-libre-3-sensors-will-be-discontinued-in-september)
***** Link (Email)
****** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=ab96c5c8edc687a50a26ba37e6a11e02239ab989 (/component/mailto/)
***** Link (READ MORE ...)
***** Link (COMMUNICATION FROM BPHC ANNOUNCING NEW AWARD TERMS)
****** https://www.340bpriceguide.net/articles-news/140-communication-from-bphc-announcing-new-award-terms (/articles-news/140-communication-from-bphc-announcing-new-award-terms)
***** Link (Print)
****** https://www.340bpriceguide.net/articles-news/140-communication-from-bphc-announcing-new-award-terms?tmpl=component&print=1&layout=default (/articles-news/140-communication-from-bphc-announcing-new-award-terms)
***** Link (Email)
****** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=749ec61a90627df993a54dc3aba86fd806f590a8 (/component/mailto/)
***** Link (READ MORE ...)
***** Link (RITE AID WINDS DOWN 340B OPERATIONS)
****** https://www.340bpriceguide.net/articles-news/139-rite-aid-winds-down-340b-operations (/articles-news/139-rite-aid-winds-down-340b-operations)
***** Link (Print)
****** https://www.340bpriceguide.net/articles-news/139-rite-aid-winds-down-340b-operations?tmpl=component&print=1&layout=default (/articles-news/139-rite-aid-winds-down-340b-operations)
***** Link (Email)
****** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=163243bbbb52af540e66579c2ba388e97194a64f (/component/mailto/)
***** Link (READ MORE ...)
***** Link (2)
****** https://www.340bpriceguide.net/articles-news?start=4 (/articles-news)
***** Link (3)
****** Articles and News - 340B Price Guide (/articles-news) [[screenshots\70c12dfea9c4bb03a97cc0c54cd7ba2e.png]]
******* Link (Home)
******* Link (Search)
******* Link (Articles)
******* Link (About)
******* Link (Contact)
******* Link (Forgot your password?)
******* Link (Forgot your username?)
******* Link (Create an account)
******* Link (2024 340B OVERSIGHT HEARING)
******** https://www.340bpriceguide.net/articles-news/130-340b-oversight-hearing (/articles-news/130-340b-oversight-hearing)
******* Link (Print)
******** https://www.340bpriceguide.net/articles-news/130-340b-oversight-hearing?tmpl=component&print=1&layout=default (/articles-news/130-340b-oversight-hearing)
******* Link (Email)
******** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=49006d072f9531acbe035124552455e2b1a1a30a (/component/mailto/)
******* Link (READ MORE ...)
******* Link (GETTING STARTED - 340B PRICE GUIDE)
******** https://www.340bpriceguide.net/articles-news/128-getting-started-340b-price-guide (/articles-news/128-getting-started-340b-price-guide)
******* Link (Print)
******** https://www.340bpriceguide.net/articles-news/128-getting-started-340b-price-guide?tmpl=component&print=1&layout=default (/articles-news/128-getting-started-340b-price-guide)
******* Link (Email)
******** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=d3b30f548365d46a780f79d4755682f42659b1a3 (/component/mailto/)
******* Link (ONGOING SHORTAGES OF DIABETES MEDICATION)
******** https://www.340bpriceguide.net/articles-news/127-ongoing-shortages-of-diabetes-medication (/articles-news/127-ongoing-shortages-of-diabetes-medication)
******* Link (Print)
******** https://www.340bpriceguide.net/articles-news/127-ongoing-shortages-of-diabetes-medication?tmpl=component&print=1&layout=default (/articles-news/127-ongoing-shortages-of-diabetes-medication)
******* Link (Email)
******** https://www.340bpriceguide.net/component/mailto/?tmpl=component&template=rt_chapelco_child&link=4923d1491b1a1668ebb212502df565b78f904b0c (/component/mailto/)
******* Link (Weekly Product Shortages)
******* Link (READ MORE ...)
******* Link (BASAGLAR NO LONGER COVERED THROUGH PACIFIC SOURCE AND TRILLIUM.)
******** Basaglar no longer covered through Pacific Source and Trillium. - 340B Price Guide (/articles-news/125-basaglar-no-longer-be-covered-through-pacific-source) [[screenshots\65c0986f562385e0ead5ff491b44e423.png]]
********* Link (Home)
********* Link (Search)
********* Link (Articles)
********* Link (About)
********* Link (Contact)
********* Link (Forgot your password?)
********* Link (Forgot your username?)
********* Link (Create an account)
********* Link (BASAGLAR NO LONGER COVERED THROUGH PACIFIC SOURCE AND TRILLIUM.)
********* Link (Print)
********** Basaglar no longer covered through Pacific Source and Trillium. - 340B Price Guide (/articles-news/125-basaglar-no-longer-be-covered-through-pacific-source) [[screenshots\783287254b3d0058247e85dfae4f4a4d.png]]
*********** Link (Basaglar no longer covered through Pacific Source and Trillium.)
*********** Link (Print)
********* Link (Email)
********** 340B Price Guide (/component/mailto/) [[screenshots\93583a54e8fed375c1f7cac1bab054c8.png]]
*********** Button: Send
*********** Button: Cancel
********* Link (Home)
********* Link (About Us)
********* Link (Articles & News)
********* Link (Contact Us)
********** Contact Us - 340B Price Guide (/index.php/contact-us) [[screenshots\8549f052ae54405465fdb32da548f706.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (Print)
************ Contact Us - 340B Price Guide (/contact-us) [[screenshots\2f184cb745a6d17a87c3305b69123a1c.png]]
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\ab1c36a351cf559c5f771b8f61abf9ae.png]]
************* Button: Send
************* Button: Cancel
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (TOP)
********* Button: Sign up / Sign in
********* Button: Go
******* Link (Print)
******* Link (Email)
******* Link (READ MORE ...)
******* Link (Start)
******* Link (Prev)
******* Link (1)
******* Link (2)
******* Link (4)
******** Articles and News - 340B Price Guide (/articles-news) [[screenshots\8ce6de17ce123da6b8f6e62d2f4380c0.png]]
********* Link (Home)
********* Link (Search)
********* Link (Articles)
********* Link (About)
********* Link (Contact)
********* Link (Forgot your password?)
********* Link (Forgot your username?)
********* Link (Create an account)
********* Link (HEALTH CENTERS MOVE TO DISMISS CHALLENGE TO CONTRACT PHARMACY LAW)
********** Health Centers Move to Dismiss Challenge to Contract Pharmacy Law - 340B Price Guide (/articles-news/123-health-centers-move-to-dismiss-challenge-to-contract-pharmacy-law) [[screenshots\79821a1db08d3615eafee02c974afcd4.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (HEALTH CENTERS MOVE TO DISMISS CHALLENGE TO CONTRACT PHARMACY LAW)
*********** Link (Print)
************ Health Centers Move to Dismiss Challenge to Contract Pharmacy Law - 340B Price Guide (/articles-news/123-health-centers-move-to-dismiss-challenge-to-contract-pharmacy-law) [[screenshots\08fd81e47f5390f911f1dd132ce00bcb.png]]
************* Link (Health Centers Move to Dismiss Challenge to Contract Pharmacy Law)
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\b662be141063cdc8efbbdcf4ffa94429.png]]
************* Button: Send
************* Button: Cancel
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (Print)
********* Link (Email)
********* Link (READ MORE ...)
********* Link (GSK TO DISCONTINUE BRANDED FLOVENT)
********** GSK to Discontinue Branded Flovent - 340B Price Guide (/articles-news/121-gsk-to-discontinue-branded-flovent) [[screenshots\2423aaa1559fbe867f2040061107cfcf.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (GSK TO DISCONTINUE BRANDED FLOVENT)
*********** Link (Print)
************ GSK to Discontinue Branded Flovent - 340B Price Guide (/articles-news/121-gsk-to-discontinue-branded-flovent) [[screenshots\7433364aaf83c3bedb5af1bd408a856d.png]]
************* Link (GSK to Discontinue Branded Flovent)
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\e807f266fb781fb321d9e02d977036f1.png]]
************* Button: Send
************* Button: Cancel
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (Print)
********* Link (Email)
********* Link (READ MORE ...)
********* Link (RITE AID CORP. ANNOUNCES CLOSURE OF OREGON PHARMACIES)
********** Rite Aid Corp. Announces Closure of Oregon Pharmacies - 340B Price Guide (/articles-news/120-rite-aid-corp-announces-closure-of-oregon-pharmacies) [[screenshots\3e34a71402b864822e41616d51ea663a.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (RITE AID CORP. ANNOUNCES CLOSURE OF OREGON PHARMACIES)
*********** Link (Print)
************ Rite Aid Corp. Announces Closure of Oregon Pharmacies - 340B Price Guide (/articles-news/120-rite-aid-corp-announces-closure-of-oregon-pharmacies) [[screenshots\f4f58a36663b209255a255a4c409d58e.png]]
************* Link (Rite Aid Corp. Announces Closure of Oregon Pharmacies)
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\f60d388f91a7adfc8e0dcd84d53d5c68.png]]
************* Button: Send
************* Button: Cancel
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (Print)
********* Link (Email)
********* Link (READ MORE ...)
********* Link (ELI LILLY FORCED TO REMOVE RESTRICTIONS)
********** Eli Lilly Forced To Remove Restrictions - 340B Price Guide (/articles-news/119-eli-lilly-forced-to-remove-restrictions) [[screenshots\a756dbe0c914d1b2775e471536bdfa51.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (ELI LILLY FORCED TO REMOVE RESTRICTIONS)
*********** Link (Print)
************ Eli Lilly Forced To Remove Restrictions - 340B Price Guide (/articles-news/119-eli-lilly-forced-to-remove-restrictions) [[screenshots\3b29e4270cdf3254a135453d420144ea.png]]
************* Link (Eli Lilly Forced To Remove Restrictions)
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\f22e3c20f65f0286a30c2e77467899f4.png]]
************* Button: Send
************* Button: Cancel
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (Print)
********* Link (Email)
********* Link (READ MORE ...)
********* Link (Start)
********* Link (Prev)
********* Link (1)
********* Link (2)
********* Link (3)
********* Link (5)
********** Articles and News - 340B Price Guide (/articles-news) [[screenshots\32e5997e6ee0b8af25add1384296e4e3.png]]
*********** Link (Home)
*********** Link (Search)
*********** Link (Articles)
*********** Link (About)
*********** Link (Contact)
*********** Link (Forgot your password?)
*********** Link (Forgot your username?)
*********** Link (Create an account)
*********** Link (NOVO NORDISK WILL DISCONTINUE LEVEMIR)
************ Novo Nordisk will discontinue Levemir - 340B Price Guide (/articles-news/118-novo-nordisk-will-discontinue-levemir) [[screenshots\c73908edb0899c397a3dec97786aea1b.png]]
************* Link (Home)
************* Link (Search)
************* Link (Articles)
************* Link (About)
************* Link (Contact)
************* Link (Forgot your password?)
************* Link (Forgot your username?)
************* Link (Create an account)
************* Link (NOVO NORDISK WILL DISCONTINUE LEVEMIR)
************* Link (Print)
************** Novo Nordisk will discontinue Levemir - 340B Price Guide (/articles-news/118-novo-nordisk-will-discontinue-levemir) [[screenshots\a4704f6743f034b1010242061d666523.png]]
*************** Link (Novo Nordisk will discontinue Levemir)
*************** Link (Print)
************* Link (Email)
************** 340B Price Guide (/component/mailto/) [[screenshots\8d449c96d8cc101e82f34d07644832fd.png]]
*************** Button: Send
*************** Button: Cancel
************* Link (Home)
************* Link (About Us)
************* Link (Articles & News)
************* Link (Contact Us)
************* Link (TOP)
************* Button: Sign up / Sign in
************* Button: Go
*********** Link (Print)
*********** Link (Email)
*********** Link (READ MORE ...)
*********** Link (JUDGE STRIKES DOWN HRSA 340B PATIENT DEFINITION)
************ Judge Strikes Down HRSA 340B Patient Definition - 340B Price Guide (/articles-news/114-judge-strikes-down-hrsa-340b-patient-definition) [[screenshots\4847e42b391b187ba5a32fde4d5a9689.png]]
************* Link (Home)
************* Link (Search)
************* Link (Articles)
************* Link (About)
************* Link (Contact)
************* Link (Forgot your password?)
************* Link (Forgot your username?)
************* Link (Create an account)
************* Link (JUDGE STRIKES DOWN HRSA 340B PATIENT DEFINITION)
************* Link (Print)
************** Judge Strikes Down HRSA 340B Patient Definition - 340B Price Guide (/articles-news/114-judge-strikes-down-hrsa-340b-patient-definition) [[screenshots\91f2dd5fd7dc057438d72f979f3fe887.png]]
*************** Link (Judge Strikes Down HRSA 340B Patient Definition)
*************** Link (Print)
************* Link (Email)
************** 340B Price Guide (/component/mailto/) [[screenshots\442b803fe71841e93e0b2e495fd106f0.png]]
*************** Button: Send
*************** Button: Cancel
************* Link (Home)
************* Link (About Us)
************* Link (Articles & News)
************* Link (Contact Us)
************* Link (TOP)
************* Button: Sign up / Sign in
************* Button: Go
*********** Link (Print)
*********** Link (Email)
*********** Link (READ MORE ...)
*********** Link (WHAT IS 340B?)
*********** Link (Print)
************ What is 340B? - 340B Price Guide (/articles-news/50-what-is-340b) [[screenshots\7db24ddc183856b4ee5aec6f9150921b.png]]
************* Link (What is 340B?)
************* Link (Print)
*********** Link (Email)
************ 340B Price Guide (/component/mailto/) [[screenshots\964e28a2f5c05e21484b4f00d05381da.png]]
************* Button: Send
************* Button: Cancel
*********** Link (READ MORE ...)
*********** Link (MEDICATIONS TO TREAT OBESITY: WHAT IS AVAILABLE?)
************ Medications to Treat Obesity: What is Available? - 340B Price Guide (/articles-news/70-medications-to-treat-obesity-what-is-available) [[screenshots\2a2bace762a1cbbae654d8383107e2cd.png]]
************* Link (Home)
************* Link (Search)
************* Link (Articles)
************* Link (About)
************* Link (Contact)
************* Link (Forgot your password?)
************* Link (Forgot your username?)
************* Link (Create an account)
************* Link (MEDICATIONS TO TREAT OBESITY: WHAT IS AVAILABLE?)
************* Link (Print)
************** Medications to Treat Obesity: What is Available? - 340B Price Guide (/articles-news/70-medications-to-treat-obesity-what-is-available) [[screenshots\b3fadd37b3593c1aadc4f3b6221966ad.png]]
*************** Link (Medications to Treat Obesity: What is Available?)
*************** Link (Print)
************* Link (Email)
************** 340B Price Guide (/component/mailto/) [[screenshots\9b9c8d0bb926d2def4051e37386a9360.png]]
*************** Button: Send
*************** Button: Cancel
************* Link (Home)
************* Link (About Us)
************* Link (Articles & News)
************* Link (Contact Us)
************* Link (TOP)
************* Button: Sign up / Sign in
************* Button: Go
*********** Link (Print)
*********** Link (Email)
*********** Link (READ MORE ...)
*********** Link (Start)
*********** Link (Prev)
*********** Link (1)
*********** Link (2)
*********** Link (3)
*********** Link (4)
*********** Link (6)
************ Articles and News - 340B Price Guide (/articles-news) [[screenshots\4dd87d63930fce8d24f7c35186f9c8f6.png]]
************* Link (Home)
************* Link (Search)
************* Link (Articles)
************* Link (About)
************* Link (Contact)
************* Link (Forgot your password?)
************* Link (Forgot your username?)
************* Link (Create an account)
************* Link (340B REGISTRATION PERIODS)
************** 340B Registration Periods - 340B Price Guide (/articles-news/13-340b-registration-period) [[screenshots\03b0be80aeb2ed1b6e239e2862b4c914.png]]
*************** Link (Home)
*************** Link (Search)
*************** Link (Articles)
*************** Link (About)
*************** Link (Contact)
*************** Link (Forgot your password?)
*************** Link (Forgot your username?)
*************** Link (Create an account)
*************** Link (340B REGISTRATION PERIODS)
*************** Link (Print)
**************** 340B Registration Periods - 340B Price Guide (/articles-news/13-340b-registration-period) [[screenshots\f0c368c86891f4356f72718a034f12e4.png]]
***************** Link (340B Registration Periods)
***************** Link (Print)
*************** Link (Email)
**************** 340B Price Guide (/component/mailto/) [[screenshots\b0a3269b77cbf89d22187dff10c8dc40.png]]
***************** Button: Send
***************** Button: Cancel
*************** Link (Home)
*************** Link (About Us)
*************** Link (Articles & News)
*************** Link (Contact Us)
*************** Link (TOP)
*************** Button: Sign up / Sign in
*************** Button: Go
************* Link (Print)
************* Link (Email)
************* Link (READ MORE ...)
************* Link (Start)
************* Link (Prev)
************* Link (1)
************* Link (2)
************* Link (3)
************* Link (4)
************* Link (5)
************* Link (Home)
************* Link (About Us)
************* Link (Articles & News)
************* Link (Contact Us)
************* Link (TOP)
************* Button: Sign up / Sign in
************* Button: Go
*********** Link (Next)
*********** Link (End)
*********** Link (340B Registration Periods)
*********** Link (Home)
*********** Link (About Us)
*********** Link (Articles & News)
*********** Link (Contact Us)
*********** Link (TOP)
*********** Button: Sign up / Sign in
*********** Button: Go
********* Link (6)
********* Link (Next)
********* Link (End)
********* Link (Novo Nordisk will discontinue Levemir)
********* Link (Judge Strikes Down HRSA 340B Patient Definition)
********* Link (What is 340B?)
********* Link (Medications to Treat Obesity: What is Available?)
********* Link (Home)
********* Link (About Us)
********* Link (Articles & News)
********* Link (Contact Us)
********* Link (TOP)
********* Button: Sign up / Sign in
********* Button: Go
******* Link (5)
******* Link (6)
******* Link (Next)
******* Link (End)
******* Link (Health Centers Move to Dismiss Challenge to Contract Pharmacy Law)
******* Link (GSK to Discontinue Branded Flovent)
******* Link (Rite Aid Corp. Announces Closure of Oregon Pharmacies)
******* Link (Eli Lilly Forced To Remove Restrictions)
******* Link (Home)
******* Link (About Us)
******* Link (Articles & News)
******* Link (Contact Us)
******* Link (TOP)
******* Button: Sign up / Sign in
******* Button: Go
***** Link (4)
***** Link (5)
***** Link (6)
***** Link (Next)
***** Link (End)
***** Link (Continued Brand Name Victoza Shortages)
****** Continued Brand Name Victoza Shortages - 340B Price Guide (/articles-news/138-continued-brand-name-victoza-shortages) [[screenshots\4b910696fc3b1abab2d7396e0e087b9c.png]]
******* Link (Home)
******* Link (Search)
******* Link (Articles)
******* Link (About)
******* Link (Contact)
******* Link (Forgot your password?)
******* Link (Forgot your username?)
******* Link (Create an account)
******* Link (CONTINUED BRAND NAME VICTOZA SHORTAGES)
******* Link (Print)
******** Continued Brand Name Victoza Shortages - 340B Price Guide (/articles-news/138-continued-brand-name-victoza-shortages) [[screenshots\f07059c46165cdb537fb5e54de644ffa.png]]
********* Link (Continued Brand Name Victoza Shortages)
********* Link (Print)
******* Link (Email)
******** 340B Price Guide (/component/mailto/) [[screenshots\a93474524452ea11a943b24b0bae7d80.png]]
********* Button: Send
********* Button: Cancel
******* Link (Home)
******* Link (About Us)
******* Link (Articles & News)
******* Link (Contact Us)
******* Link (TOP)
******* Button: Sign up / Sign in
******* Button: Go
***** Link (Weekly Update Episode 1: President Trump Healthcare Executive Order)
****** Weekly Update Episode 1: President Trump Healthcare Executive Order - 340B Price Guide (/articles-news/133-weekly-update-episode-1-president-trump-healthcare-executive-order) [[screenshots\a3f29d6feeb2955f0d4ead39bf0a1bff.png]]
******* Link (Home)
******* Link (Search)
******* Link (Articles)
******* Link (About)
******* Link (Contact)
******* Link (Forgot your password?)
******* Link (Forgot your username?)
******* Link (Create an account)
******* Link (WEEKLY UPDATE EPISODE 1: PRESIDENT TRUMP HEALTHCARE EXECUTIVE ORDER)
******* Link (Print)
******** Weekly Update Episode 1: President Trump Healthcare Executive Order - 340B Price Guide (/articles-news/133-weekly-update-episode-1-president-trump-healthcare-executive-order) [[screenshots\2c4a10279c6d85283be51cc43a3a43e8.png]]
********* Link (Weekly Update Episode 1: President Trump Healthcare Executive Order)
********* Link (Print)
******* Link (Email)
******** 340B Price Guide (/component/mailto/) [[screenshots\95e2a641a6c84d8725191fdb15a8e3e4.png]]
********* Button: Send
********* Button: Cancel
******* Link (Home)
******* Link (About Us)
******* Link (Articles & News)
******* Link (Contact Us)
******* Link (TOP)
******* Button: Sign up / Sign in
******* Button: Go
***** Link (Rite Aid halts dispensing GLP1 agonists (Ozempic/Trulicity/Victoza))
****** Rite Aid halts dispensing GLP1 agonists (Ozempic/Trulicity/Victoza) - 340B Price Guide (/articles-news/134-rite-aid-is-halts-dispensing-glp1-agonists-ozempic-trulicity-victoza) [[screenshots\6eda6a1ef39e8141dcbaf374d76c8a86.png]]
******* Link (Home)
******* Link (Search)
******* Link (Articles)
******* Link (About)
******* Link (Contact)
******* Link (Forgot your password?)
******* Link (Forgot your username?)
******* Link (Create an account)
******* Link (RITE AID HALTS DISPENSING GLP1 AGONISTS (OZEMPIC/TRULICITY/VICTOZA))
******* Link (Print)
******** Rite Aid halts dispensing GLP1 agonists (Ozempic/Trulicity/Victoza) - 340B Price Guide (/articles-news/134-rite-aid-is-halts-dispensing-glp1-agonists-ozempic-trulicity-victoza) [[screenshots\a37c26c5620f43f430df597f606e4247.png]]
********* Link (Rite Aid halts dispensing GLP1 agonists (Ozempic/Trulicity/Victoza))
********* Link (Print)
******* Link (Email)
******** 340B Price Guide (/component/mailto/) [[screenshots\9b2cd62370acd28a1c1476eac4b7b47e.png]]
********* Button: Send
********* Button: Cancel
******* Link (Home)
******* Link (About Us)
******* Link (Articles & News)
******* Link (Contact Us)
******* Link (TOP)
******* Button: Sign up / Sign in
******* Button: Go
***** Link (Mobile App - How to Use)
****** Mobile App - How to Use - 340B Price Guide (/articles-news/132-mobile-app-how-to-use) [[screenshots\b8f07ff757d95c0744b3cf044d5f0804.png]]
******* Link (Home)
******* Link (Search)
******* Link (Articles)
******* Link (About)
******* Link (Contact)
******* Link (Forgot your password?)
******* Link (Forgot your username?)
******* Link (Create an account)
******* Link (MOBILE APP - HOW TO USE)
******* Link (Print)
******** Mobile App - How to Use - 340B Price Guide (/articles-news/132-mobile-app-how-to-use) [[screenshots\5e27c4e884f9914f45b698f4cda1fe92.png]]
********* Link (Mobile App - How to Use)
********* Link (Print)
******* Link (Email)
******** 340B Price Guide (/component/mailto/) [[screenshots\eb33befa8f298acbae327d1ef07d37f3.png]]
********* Button: Send
********* Button: Cancel
******* Link (Home)
******* Link (About Us)
******* Link (Articles & News)
******* Link (Contact Us)
******* Link (TOP)
******* Button: Sign up / Sign in
******* Button: Go
***** Link (Home)
***** Link (About Us)
***** Link (Articles & News)
***** Link (Contact Us)
***** Link (TOP)
***** Button: Sign up / Sign in
***** Button: Go
*** Link (Contact Us)
*** Link (TOP)
*** Button: Sign up / Sign in
*** Button: Go
*** Button: FIND 340B PRICES
@endmindmap

"""

# Generate mind map
generate_mindmap(uml_code, "teamup_mindmap.png")
