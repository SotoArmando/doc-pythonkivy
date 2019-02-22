

class Asistente():
    Response = None
    client = None
    xml = None
    xml_string = None
    def __init__(self,**kwargs):
        from suds.client import Client
        url="http://invetco.dyndns.org:7001/ProveedorWS/ImplXmlMessageAprobationService?wsdl"
        self.client = Client(url)
        print self.client 




    def execute(self):
        token = self.client.service.GenerarTokenTr("ASOTO","8493532487")
        print "Acceso obtenido token .: ",token
        #x = self.client.service.ConsultarData("10.0.0.214","db_eRX","asoto","$a40227587850","exec SP_Clientes",token)
        x = self.client.service.ConsultarData("10.0.0.214","db_eRX","asoto","$a40227587850","SELECT XmleRx FROM eReceta",token)
        #x = self.client.service.ConsultarData("10.0.0.214","db_eRX","asoto","$a40227587850","SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'",token)

        import xml.dom.minidom
        self.xml_string = x
        self.xml = xml.dom.minidom.parseString(x) 
        pretty_xml_as_string = self.xml.toprettyxml()
        print (pretty_xml_as_string)
    def getarray(self):
        import xml.etree.ElementTree as et

        tree = et.fromstring(self.xml_string)
        #root = tree.getroot()
        # for child in root:
        #     print(child.tag, child.attrib)
        pacientes = tree.findall('PATIENT')
        for p in pacientes:
            a = p.find('PDI/PDI.5/XPN.1/FN.1').text
            b = p.find('PDI/PDI.11/XAD.3').text
            c = p.find('PDI/PDI.11/XAD.6').text
            print a,b,c
        ordenes = tree.findall('Orden')
        for orden in ordenes:
            posicion = p.find('OMP_O09/RXO/RXO.8').text
            tipo = p.find('OMP_O09/RXO/RXO.27').text
            print posicion,tipo

        # for child in tree:
            # for element in child:
                # print(element.tag, ":", element.text)

        # new_product = et.SubElement(root, "product", attrib={"id": "4"})
        # new_prod_name = et.SubElement(new_product, "name")
        # new_prod_desc = et.SubElement(new_product, "description")
        # new_prod_cost = et.SubElement(new_product, "cost")
        # new_prod_ship = et.SubElement(new_product, "shipping")

        # new_prod_name.text = "Python Pants"
        # new_prod_desc.text = "These pants will surely help you code like crazy!"
        # new_prod_cost.text = "39.95"
        # new_prod_ship.text = "4.00"

        # tree.write(xml_file)

        # for child in root:
            # print(child.tag, child.attrib)
        


Armando = Asistente()
Armando.execute()
Armando.getarray()