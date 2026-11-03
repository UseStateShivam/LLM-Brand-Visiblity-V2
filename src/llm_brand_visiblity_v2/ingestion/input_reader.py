def read_input():
    mp = {}

    brand_name = input("Enter your brand name: ")
    website = input("Enter your website: ")
    competitors_string = input("Enter your competitors(optional) comma seperated: ")
    products_string = input("Enter your products(optional) comma seperated: ")
    services_string = input("Enter your services(optional) comma seperated: ")
    niche = input("Enter your brand niche: ")

    def str_to_list(s):
        if len(s.strip()) == 0:
            return None

        l = s.split(',')

        for i in range(len(l)):
            li = l[i].strip()
            l[i] = li

        return l

    competitors = str_to_list(competitors_string)
    products = str_to_list(products_string)
    services = str_to_list(services_string)

    mp["brand_name"] = brand_name
    mp["website"] = website
    mp["competitors"] = competitors
    mp["products"] = products
    mp["services"] = services
    mp["niche"] = niche

    return mp