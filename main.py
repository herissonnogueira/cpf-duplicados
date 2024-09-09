import xml.etree.ElementTree as ET
from collections import defaultdict
from fpdf import FPDF

def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        return tree.getroot()
    except ET.ParseError as e:
        print(f"Erro ao analisar o arquivo XML: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Arquivo não encontrado: {e}")
        return None

# Dicionário de mapeamento de códigos INEP para nomes de escolas
codigo_escola_inep = {
    "28012623": "CRECHE MAE EMILIA",
    "28037561": "EMEI DULCILENE TEIXEIRA ALMEIDA",
    "28013980": "COLEGIO ESTADUAL JOSE GUIMARAES LIMA",
}

def find_cpfs(xml_root, ns):
    cpf_dict = defaultdict(list)
    total_cpfs = 0

    for escola in xml_root.findall('edu:escola', ns):
        codigo_escola = escola.find('edu:idEscola', ns).text
        nome_escola = codigo_escola_inep.get(codigo_escola, "Nome não encontrado")  # Obter o nome da escola correspondente ao código INEP
        escola_info = f"{codigo_escola} | {nome_escola}"
        for turma in escola.findall('edu:turma', ns):
            nome_turma = turma.find('edu:descricao', ns).text
            modalidade_relevante = any(
                serie.find('edu:modalidade', ns).text in {'1', '2', '3', '4'} 
                for serie in turma.findall('edu:serie', ns)
            )
            if modalidade_relevante:
                for matricula in turma.findall('edu:matricula', ns):
                    aluno = matricula.find('edu:aluno', ns)
                    if aluno is not None:
                        cpf = aluno.find('edu:cpfAluno', ns)
                        nome_aluno = aluno.find('edu:nome', ns).text
                        if cpf is not None:
                            cpf_dict[cpf.text].append((escola_info, nome_turma, nome_aluno))
                            total_cpfs += 1
    
    duplicate_cpfs = {cpf: dados for cpf, dados in cpf_dict.items() if len(dados) > 1}
    return duplicate_cpfs, total_cpfs

def write_output_to_text(duplicate_cpfs, total_cpfs, output_file):
    total_duplicates = len(duplicate_cpfs)
    with open(output_file, 'w', encoding='utf-8') as file:
        for cpf, dados in duplicate_cpfs.items():
            file.write(f"CPF: {cpf}\n")
            for escola_info, nome_turma, nome in dados:
                file.write(f"  ID da Escola: {escola_info}\n")
                file.write(f"  Nome da Turma: {nome_turma}\n")
                file.write(f"  Nome: {nome}\n")
            file.write("\n")
        file.write(f"Total de CPFs duplicados: {total_duplicates}\n")
        file.write(f"Total de CPFs encontrados: {total_cpfs}\n")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 14)
        self.cell(0, 10, "Relatório de CPFs Duplicados", 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def add_duplicate_cpf(self, cpf, dados):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, f"CPF: {cpf}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
        self.set_font("Arial", '', 12)
        for escola_info, nome_turma, nome in dados:
            self.cell(0, 10, f"  ID da Escola: {escola_info}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
            self.cell(0, 10, f"  Nome da Turma: {nome_turma}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
            self.cell(0, 10, f"  Nome: {nome}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
        self.ln(5)

def write_output_to_pdf(duplicate_cpfs, total_cpfs, output_file):
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_auto_page_break(auto=True, margin=15)
    
    total_duplicates = len(duplicate_cpfs)
    
    for cpf, dados in duplicate_cpfs.items():
        pdf.add_duplicate_cpf(cpf, dados)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Total de CPFs duplicados: {total_duplicates}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
    pdf.cell(0, 10, f"Total de CPFs encontrados: {total_cpfs}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
    
    pdf.output(output_file)

def main(xml_file, text_output_file, pdf_output_file):
    ns = {'edu': 'http://www.tce.se.gov.br/sagres2022/xml/sagresEdu'}
    xml_root = parse_xml(xml_file)
    if xml_root is not None:
        duplicate_cpfs, total_cpfs = find_cpfs(xml_root, ns)
        write_output_to_text(duplicate_cpfs, total_cpfs, text_output_file)
        write_output_to_pdf(duplicate_cpfs, total_cpfs, pdf_output_file)

if __name__ == "__main__":
    xml_file = 'Educacao_Exemplo_v2.xml'
    text_output_file = 'cpfs_duplicados.txt'
    pdf_output_file = 'cpfs_duplicados.pdf'
    main(xml_file, text_output_file, pdf_output_file)
