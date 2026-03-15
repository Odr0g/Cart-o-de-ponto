import tkinter as tk
from tkinter import messagebox
import hashlib
from datetime import datetime, date, timedelta
import calendar
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas


totais_labels = []
extras_labels = []
atraso_labels = []

numero = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

senha_mestra = "Ptnqmftc3002Mter"
senha_mestra_hash = hashlib.sha256(senha_mestra.encode()).hexdigest()

FONTE_TITULO = ("Segoe UI", 16, "bold")
FONTE_TEXTO = ("Segoe UI", 11)
FONTE_BOTAO = ("Segoe UI", 11, "bold")

COR_FUNDO = "#f4f6f8"
COR_BOTAO = "#1976d2"
COR_BOTAO_TEXTO = "#ffffff"
COR_INPUT = "#ffffff"

def design_janela(janela_design, titulo, tamanho):#configuração de design das janelas
    janela_design.title(titulo)
    janela_design.geometry(tamanho)
    janela_design.configure(bg=COR_FUNDO)

################################################## TODA A PARTE DE LOGIN E CADASTRO ########################################################################

def janela_cadastro():
    janela_acesso = tk.Toplevel()
    design_janela(janela_acesso, "Cadastro de Usuário", "400x350")

    tk.Label(janela_acesso,text="Cadastro",font=FONTE_TITULO,bg=COR_FUNDO).pack(pady=15)


    def cadastro():#dados de entrada do cadastro
        nome = entry_nome.get().strip()
        senha = entry_senha.get().strip()

        if nome == "":
            messagebox.showerror("Erro", "Digite seu nome.")
            return

        if len(senha) < 6 or not any(n in senha for n in numero):
            messagebox.showerror("Erro","A senha deve conter ao menos 1 número e ter mais que 6 caracteres.")
            return
        
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        abrir_janela_senha_mestra(nome, senha_hash)
        janela_acesso.destroy()

    tk.Label(janela_acesso, text="Nome", font=FONTE_TEXTO, bg=COR_FUNDO).pack()
    entry_nome = tk.Entry(janela_acesso, font=FONTE_TEXTO, width=30, bg=COR_INPUT)
    entry_nome.pack(pady=5)

    tk.Label(janela_acesso, text="Senha", font=FONTE_TEXTO, bg=COR_FUNDO).pack()
    entry_senha = tk.Entry(janela_acesso, show="*", font=FONTE_TEXTO, width=30, bg=COR_INPUT)
    entry_senha.pack(pady=5)

    tk.Button(janela_acesso,text="Confirmar",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=20,command=cadastro).pack(pady=20)


    entry_nome.delete(0, tk.END)
    entry_senha.delete(0, tk.END)


def abrir_janela_senha_mestra(nome, senha_hash):#janela para colocar senha mestra e validar o cadastro
    janela_master = tk.Toplevel()
    design_janela(janela_master, "Senha Mestra", "400x250")

    def validar_senha_mestra():
        senha_digitada = entry_master.get().strip()
        senha_digitada_hash = hashlib.sha256(senha_digitada.encode()).hexdigest()#conversão da senha para buscar ela com o hash

        entry_master.delete(0, tk.END)

        if senha_digitada_hash != senha_mestra_hash:
            messagebox.showerror("Erro", "Senha mestra incorreta!")
            return

        with open("contas.csv", "a",encoding="utf-8") as f:
            f.write(f"{nome},{senha_hash}\n")
        
        with open(f"conta_{nome}.csv", "w",encoding="utf-8") as f:
            f.write(f"{nome},{senha_hash}\n")

        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        janela_master.destroy()


    tk.Label(janela_master,text="Confirmação Administrativa",font=FONTE_TITULO,bg=COR_FUNDO).pack(pady=15)

    tk.Label(janela_master, text="Senha Mestra", font=FONTE_TEXTO, bg=COR_FUNDO).pack()
    entry_master = tk.Entry(janela_master, show="*", font=FONTE_TEXTO, width=30)
    entry_master.pack(pady=10)

    tk.Button(janela_master,text="Validar",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=20,command=validar_senha_mestra).pack(pady=15)


def login():#janela de login
    janela_login = tk.Toplevel()
    design_janela(janela_login, "Login", "400x300")

    def entrar():#entrada de dados
        nome_digitado = entry_nome.get().strip()
        senha_digitada = entry_senha.get().strip()

        entry_nome.delete(0, tk.END)
        entry_senha.delete(0, tk.END)

        senha_digitada_hash = hashlib.sha256(senha_digitada.encode()).hexdigest()#conversão da senha para buscar ela com o hash

        with open("contas.csv", "r", encoding="utf-8") as f:
            linhas = f.readlines()

        encontrado = False

        for linha in linhas:
            partes = linha.strip().split(",")
            if len(partes) >= 2:#busca dos dados no arquivo
                if partes[0] == nome_digitado and partes[1] == senha_digitada_hash:
                    encontrado = True
                    break

        if encontrado:
            messagebox.showinfo("Login", "Bem-vindo!")
            janela_login.destroy()
            janela_planilha_ponto()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    
    tk.Label(janela_login,text="Login",font=FONTE_TITULO,bg=COR_FUNDO).pack(pady=15)

    tk.Label(janela_login, text="Usuário", font=FONTE_TEXTO, bg=COR_FUNDO).pack()
    entry_nome = tk.Entry(janela_login, font=FONTE_TEXTO, width=30)
    entry_nome.pack(pady=5)

    tk.Label(janela_login, text="Senha", font=FONTE_TEXTO, bg=COR_FUNDO).pack()
    entry_senha = tk.Entry(janela_login, show="*", font=FONTE_TEXTO, width=30)
    entry_senha.pack(pady=5)

    tk.Button(janela_login,text="Entrar",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=20,command=entrar).pack(pady=20)

################################################## SOMA DAS HORAS ######################################################################
def minutos_para_horas(minutos):#conversão
    try:
        minutos = int(minutos)
        horas = minutos // 60
        mins = minutos % 60
        return f"{horas:02d}:{mins:02d}"
    except:
        return "00:00"


def horas_para_minutos(hora):#conversão
    try:
        h, m = hora.split(":")
        return int(h) * 60 + int(m)
    except:
        return 0


def janela_planilha_ponto():#Interface cartão
    janela_planilha = tk.Toplevel()
    janela_planilha.title("Cartão de Ponto")
    janela_planilha.geometry("800x600")

    canvas = tk.Canvas(janela_planilha)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(janela_planilha, orient="vertical", command=canvas.yview)#configurando a scroll bar
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
   #Espaço para colocar o nome do funcionario 
    tk.Label(frame, text="Funcionário:", font=FONTE_TEXTO).grid(row=0, column=0, sticky="w", pady=5)

    entry_funcionario = tk.Entry(frame, font=FONTE_TEXTO, width=30)
    entry_funcionario.grid(row=0, column=1, columnspan=3, sticky="w", pady=5)


    hoje = date.today()#Aplicando a biblioteca, definindo data atual
    ano = hoje.year
    mes = hoje.month

    total_dias_mes = calendar.monthrange(ano, mes)[1]
    data_atual = date(ano, mes, 1)

    linha = 1
    for _ in range(total_dias_mes):

        tk.Label(frame,text=data_atual.strftime("%d/%m/%Y")).grid(row=linha, column=0)

    # Cabeçalho
    tk.Label(frame, text="Data").grid(row=1, column=0)
    tk.Label(frame, text="E1").grid(row=1, column=1)
    tk.Label(frame, text="S1").grid(row=1, column=2)
    tk.Label(frame, text="E2").grid(row=1, column=3)
    tk.Label(frame, text="S2").grid(row=1, column=4)
    tk.Label(frame, text="Total").grid(row=1, column=5)
    tk.Label(frame, text="Extra").grid(row=1, column=6)
    tk.Label(frame, text="Atraso").grid(row=1, column=7)
    tk.Label(frame, text="").grid(row=1, column=8)


    linha = 2
    for _ in range(total_dias_mes):#Aqui é um loop da interface do cartão de ponta, gera labels de acordo aos dias do mês

        tk.Label(frame,text=data_atual.strftime("%d/%m/%Y"),width=10).grid(row=linha, column=0)

        entry_e1 = tk.Entry(frame, width=6, justify="center")
        entry_s1 = tk.Entry(frame, width=6, justify="center")
        entry_e2 = tk.Entry(frame, width=6, justify="center")
        entry_s2 = tk.Entry(frame, width=6, justify="center")

        entry_e1.grid(row=linha, column=1)
        entry_s1.grid(row=linha, column=2)
        entry_e2.grid(row=linha, column=3)
        entry_s2.grid(row=linha, column=4)

        lbl_total = tk.Label(frame, text="00:00", width=6, relief="solid")
        lbl_extra = tk.Label(frame, text="00:00", width=6, relief="solid")
        lbl_atraso = tk.Label(frame, text="00:00", width=6, relief="solid")

        lbl_total.grid(row=linha, column=5)
        lbl_extra.grid(row=linha, column=6)
        lbl_atraso.grid(row=linha, column=7)

        # guarda os labels para soma mensal
        totais_labels.append(lbl_total)
        extras_labels.append(lbl_extra)
        atraso_labels.append(lbl_atraso)

        def salvar_cartao():
            nome = entry_funcionario.get().strip()

            if not nome:
                messagebox.showerror("Erro", "Digite o nome do funcionário.")
                return

            nome_arquivo = nome.replace(" ", "_").upper()
            arquivo = f"ponto_{nome_arquivo}_{mes:02d}-{ano}.csv"

            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("Data,E1,S1,E2,S2,Total,Extra\n")

                for i in range(len(totais_labels)):
                    data = frame.grid_slaves(row=i+2, column=0)[0].cget("text")
                    total = totais_labels[i].cget("text")
                    extra = extras_labels[i].cget("text")
                    atraso = atraso_labels[i].cget("text")

                    f.write(f"{data},,,,{total},{extra},{atraso}\n")


            def gerar_pdf():
                nome = entry_funcionario.get().strip()

                if not nome:
                    messagebox.showerror("Erro", "Digite o nome do funcionário.")
                    return

                nome_arquivo = nome.replace(" ", "_").upper()
                arquivo = f"ponto_{nome_arquivo}_{mes:02d}-{ano}.pdf"

                c = pdf_canvas.Canvas(arquivo, pagesize=A4)
                largura, altura = A4

                y = altura - 50

                # Título
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y, "Cartão de Ponto")
                y -= 25

                c.setFont("Helvetica", 11)
                c.drawString(50, y, f"Funcionário: {nome}")
                y -= 20

                c.drawString(50, y, f"Mês/Ano: {mes:02d}/{ano}")
                y -= 30

                # Cabeçalho da tabela
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, y, "Data")
                c.drawString(120, y, "Total")
                c.drawString(180, y, "Extra")
                c.drawString(240, y, "Atraso")
                y -= 15

                c.setFont("Helvetica", 10)

                for i in range(len(totais_labels)):
                    data = frame.grid_slaves(row=i+2, column=0)[0].cget("text")
                    total = totais_labels[i].cget("text")
                    extra = extras_labels[i].cget("text")
                    atraso = atraso_labels[i].cget("text")

                    c.drawString(50, y, data)
                    c.drawString(120, y, total)
                    c.drawString(180, y, extra)
                    c.drawString(240, y, atraso)

                    y -= 14

                    if y < 50:
                        c.showPage()
                        y = altura - 50
                        c.setFont("Helvetica", 10)

                # Totais finais
                y -= 20
                c.setFont("Helvetica-Bold", 11)
                c.drawString(50, y, f"Total de Horas: {lbl_total_geral.cget('text')}")
                y -= 20
                c.drawString(50, y, f"Total de Extra: {lbl_extra_geral.cget('text')}")
                y -= 20
                c.drawString(50, y, f"Total de Atraso: {lbl_atraso_geral.cget('text')}")

                c.save()
            
            gerar_pdf()
            messagebox.showinfo("PDF Gerado", f"Arquivo criado:\n{arquivo}")
            janela_planilha.destroy()

        def calcular_linha(e1=entry_e1,s1=entry_s1,e2=entry_e2,s2=entry_s2,total_lbl=lbl_total,extra_lbl=lbl_extra,atraso_lbl=lbl_atraso):
            try:
                d1 = datetime.strptime(e1.get(), "%H:%M")
                d2 = datetime.strptime(s1.get(), "%H:%M")
                d3 = datetime.strptime(e2.get(), "%H:%M")
                d4 = datetime.strptime(s2.get(), "%H:%M")

                total = (d2 - d1) + (d4 - d3)
                minutos = int(total.total_seconds() / 60)

                jornada = 7 * 60 + 20
                extra = max(0, minutos - jornada)

                atraso = max(0, jornada - minutos)

                total_lbl.config(text=minutos_para_horas(minutos))
                extra_lbl.config(text=minutos_para_horas(extra))
                atraso_lbl.config(text=minutos_para_horas(atraso))
                

            except:
                total_lbl.config(text="00:00")
                extra_lbl.config(text="00:00")
                atraso_lbl.config(text="00:00")

        tk.Button(frame, text="Calcular", command=calcular_linha).grid(row=linha, column=8)

        data_atual += timedelta(days=1)
        linha += 1

    tk.Label(frame, text="Total de Horas").grid(row=linha, column=1)
    tk.Label(frame, text="Total de Extra").grid(row=linha, column=4)
    tk.Label(frame, text="Total de Atraso").grid(row=linha, column=6)

    lbl_total_geral = tk.Label(frame, text="00:00", width=8, relief="solid")
    lbl_extra_geral = tk.Label(frame, text="00:00", width=8, relief="solid")
    lbl_atraso_geral = tk.Label(frame, text="00:00", width=8, relief="solid")

    lbl_total_geral.grid(row=linha, column=2)
    lbl_extra_geral.grid(row=linha, column=5)
    lbl_atraso_geral.grid(row=linha, column=7)

    linha += 1

    def somar_totais():
        total_min = 0
        extra_min = 0
        atraso_min = 0

        for lbl in totais_labels:
            total_min += horas_para_minutos(lbl.cget("text"))

        for lbl in extras_labels:
            extra_min += horas_para_minutos(lbl.cget("text"))

        for lbl in atraso_labels:
            atraso_min += horas_para_minutos(lbl.cget("text"))

        lbl_total_geral.config(text=minutos_para_horas(total_min))
        lbl_extra_geral.config(text=minutos_para_horas(extra_min))
        lbl_atraso_geral.config(text=minutos_para_horas(atraso_min))

    tk.Button(frame,text="Somar Totais",command=somar_totais,width=15).grid(row=linha, column=2, columnspan=2, pady=5)

    linha +=1

    tk.Button(frame,text="Salvar Cartão",command=salvar_cartao,font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=15).grid(row=linha, column=2, columnspan=2, pady=5)

    confirmar_saida(janela_planilha)
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    
def confirmar_saida(janela):
    def confirmar():
        resposta = messagebox.askyesno("Atenção", "Deseja sair?")
        if resposta:
            janela.destroy()
    janela.protocol("WM_DELETE_WINDOW", confirmar)
    return confirmar

janela_menu = tk.Tk()
janela_menu.title("Cartão de Ponto")
janela_menu.geometry("800x600")
janela_menu.configure(bg=COR_FUNDO)

tk.Label(janela_menu,text="Cartão de Ponto",font=FONTE_TITULO,bg=COR_FUNDO).pack(pady=20)

tk.Label(janela_menu,text="Se for seu primeiro acesso, cadastre um usuário",font=FONTE_TEXTO,bg=COR_FUNDO).pack(pady=10)

tk.Button(janela_menu,text="Cadastrar Usuário",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=25,height=2,command=janela_cadastro).pack(pady=10)

tk.Button(janela_menu,text="Já possuo cadastro",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=25,height=2,command=login).pack(pady=10)

tk.Button(janela_menu,text="Sair",font=FONTE_BOTAO,bg=COR_BOTAO,fg=COR_BOTAO_TEXTO,width=25,height=2,command=confirmar_saida(janela_menu)).pack(pady=10)

janela_menu.mainloop()