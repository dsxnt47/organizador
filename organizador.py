import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import threading
import time


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class OrganizadorArquivos(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organizador de Arquivos")
        self.geometry("700x600")
        
        self.pasta_alvo = ""
        
        
        self.categorias = {
            "📁 Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
            "🖼️ Imagens": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".bmp"],
            "🎥 Videos e Audios": [".mp4", ".avi", ".mkv", ".mp3", ".wav"],
            "📦 Compactados e Instaladores": [".zip", ".rar", ".7z", ".exe", ".msi"]
        }

        self.criar_interface()

    def criar_interface(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        
        lbl_titulo = ctk.CTkLabel(self, text="Organizador Inteligente de Pastas", font=("Roboto", 26, "bold"), text_color="#2ecc71")
        lbl_titulo.grid(row=0, column=0, pady=(20, 5))

        lbl_sub = ctk.CTkLabel(self, text="Diga adeus à bagunça. Organize milhares de arquivos em segundos.", font=("Roboto", 14), text_color="gray")
        lbl_sub.grid(row=1, column=0, pady=(0, 20))

        
        frame_selecao = ctk.CTkFrame(self, fg_color="transparent")
        frame_selecao.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        frame_selecao.grid_columnconfigure(0, weight=1)

        self.txt_caminho = ctk.CTkEntry(frame_selecao, font=("Roboto", 12), placeholder_text="Nenhuma pasta selecionada...")
        self.txt_caminho.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        self.txt_caminho.configure(state="readonly") 

        btn_selecionar = ctk.CTkButton(frame_selecao, text="📂 Escolher Pasta", command=self.selecionar_pasta, font=("Roboto", 12, "bold"))
        btn_selecionar.grid(row=0, column=1)

        
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 12), fg_color="#1e1e1e", text_color="#00ff00")
        self.log_box.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.log_box.insert(tk.END, ">>> Sistema pronto. Aguardando seleção de pasta...\n")
        self.log_box.configure(state="disabled")

        
        self.btn_organizar = ctk.CTkButton(self, text="🚀 INICIAR FAXINA", font=("Roboto", 16, "bold"), height=50, command=self.iniciar_organizacao, fg_color="#d35400", hover_color="#e67e22")
        self.btn_organizar.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.barra_progresso = ctk.CTkProgressBar(self, mode="determinate", progress_color="#2ecc71")
        self.barra_progresso.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.barra_progresso.set(0)
        self.barra_progresso.grid_remove()

    def escrever_log(self, texto):
        """Função para escrever no terminalzinho da tela"""
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, texto + "\n")
        self.log_box.see(tk.END) 
        self.log_box.configure(state="disabled")

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta bagunçada")
        if pasta:
            self.pasta_alvo = pasta
            self.txt_caminho.configure(state="normal")
            self.txt_caminho.delete(0, tk.END)
            self.txt_caminho.insert(0, self.pasta_alvo)
            self.txt_caminho.configure(state="readonly")
            self.escrever_log(f">>> Pasta selecionada: {self.pasta_alvo}")

    def iniciar_organizacao(self):
        if not self.pasta_alvo:
            messagebox.showwarning("Aviso", "Selecione uma pasta primeiro!")
            return

        self.btn_organizar.configure(state="disabled", text="ORGANIZANDO...")
        self.barra_progresso.grid()
        self.barra_progresso.set(0)
        
        
        threading.Thread(target=self.rotina_organizacao, daemon=True).start()

    def rotina_organizacao(self):
        try:
           
            arquivos = [arq for arq in os.listdir(self.pasta_alvo) if os.path.isfile(os.path.join(self.pasta_alvo, arq))]
            total_arquivos = len(arquivos)

            if total_arquivos == 0:
                self.escrever_log(">>> Nenhum arquivo solto encontrado nesta pasta.")
                self.finalizar_rotina()
                return

            self.escrever_log(f">>> Iniciando organização de {total_arquivos} arquivos...\n")
            
            arquivos_movidos = 0

            for index, arquivo in enumerate(arquivos):
                caminho_origem = os.path.join(self.pasta_alvo, arquivo)
                _, extensao = os.path.splitext(arquivo)
                extensao = extensao.lower()

                pasta_destino_nome = "Outros" 

               
                for categoria, extensoes_validas in self.categorias.items():
                    if extensao in extensoes_validas:
                        pasta_destino_nome = categoria
                        break

                caminho_destino = os.path.join(self.pasta_alvo, pasta_destino_nome)

                
                if not os.path.exists(caminho_destino):
                    os.makedirs(caminho_destino)
                    self.escrever_log(f"[+] Pasta criada: {pasta_destino_nome}")

               
                caminho_final = os.path.join(caminho_destino, arquivo)
                
                
                if not os.path.exists(caminho_final):
                    shutil.move(caminho_origem, caminho_destino)
                    self.escrever_log(f"[OK] Movido -> {arquivo}")
                    arquivos_movidos += 1
                else:
                    self.escrever_log(f"[ALERTA] Já existe -> {arquivo}. Ignorado.")

              
                progresso_atual = (index + 1) / total_arquivos
                self.barra_progresso.set(progresso_atual)
                
               
                time.sleep(0.02) 

            self.escrever_log(f"\n>>> SUCESSO! {arquivos_movidos} arquivos organizados.")
            messagebox.showinfo("Concluído", f"Faxina concluída!\n{arquivos_movidos} arquivos foram organizados.")

        except Exception as e:
            self.escrever_log(f"[ERRO CRÍTICO] {str(e)}")
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{str(e)}")

        finally:
            self.finalizar_rotina()

    def finalizar_rotina(self):
        self.btn_organizar.configure(state="normal", text="🚀 INICIAR FAXINA")
        self.barra_progresso.grid_remove()

if __name__ == "__main__":
    app = OrganizadorArquivos()
    app.mainloop()