import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sqlite3

class Kitap:
    def __init__(self, adi, yazar, yayinevi, icerik):
        self.adi = adi
        self.yazar = yazar
        self.yayinevi = yayinevi
        self.icerik = icerik

    def kitap_ekle(self):
        # Kitabı platforma ekler
        with sqlite3.connect("kitaplar.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO kitaplar (adi, yazar, yayinevi, icerik) VALUES (?, ?, ?, ?)",
                           (self.adi, self.yazar, self.yayinevi, self.icerik))
            conn.commit()

class AnaPencere(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Çevrimiçi Kitap Okuma ve Paylaşım Platformu")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Karanlık tema için 'clam' kullanıyoruz
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TText", font=("Helvetica", 12))

        self.create_widgets()

    def create_widgets(self):
        self.label_baslik = ttk.Label(self, text="Çevrimiçi Kitap Okuma ve Paylaşım Platformu",
                                      font=("Helvetica", 20, "bold"))
        self.label_baslik.pack(pady=10)

        self.frame_giris = ttk.Frame(self)
        self.label_kullanici_adi = ttk.Label(self.frame_giris, text="Kullanıcı Adı:", font=("Helvetica", 12))
        self.label_kullanici_adi.grid(row=0, column=0, padx=5, pady=5)
        self.entry_kullanici_adi = ttk.Entry(self.frame_giris, font=("Helvetica", 12))
        self.entry_kullanici_adi.grid(row=0, column=1, padx=5, pady=5)

        self.label_sifre = ttk.Label(self.frame_giris, text="Şifre:", font=("Helvetica", 12))
        self.label_sifre.grid(row=1, column=0, padx=5, pady=5)
        self.entry_sifre = ttk.Entry(self.frame_giris, show="*", font=("Helvetica", 12))
        self.entry_sifre.grid(row=1, column=1, padx=5, pady=5)

        self.button_giris = ttk.Button(self.frame_giris, text="Giriş Yap", command=self.giris_yap)
        self.button_giris.grid(row=2, column=0, columnspan=2, pady=5)

        self.button_kayit = ttk.Button(self.frame_giris, text="Kayıt Ol", command=self.kayit_penceresi_ac)
        self.button_kayit.grid(row=3, column=0, columnspan=2, pady=5)

        self.frame_giris.pack(pady=20)

        self.button_kilavuz = ttk.Button(self, text="Kullanım Kılavuzu", command=self.kilavuz_ac)
        self.button_kilavuz.place(relx=0.05, rely=0.9)

    def giris_yap(self):
        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()
        with sqlite3.connect("kitaplar.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kullanicilar WHERE kullanici_adi=? AND sifre=?", (kullanici_adi, sifre))
            kullanici = cursor.fetchone()
            if kullanici:
                self.destroy()
                AnaIslemPencere(kullanici_adi)
            else:
                messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")

    def kayit_penceresi_ac(self):
        self.kayit_penceresi = KayitPenceresi(self)

    def kilavuz_ac(self):
        kullanım_kılavuzu = """
                Kullanım Kılavuzu:

        1. Kayıt Ol: Kullanıcı adı ve şifre belirleyerek kayıt olabilirsiniz.
        
        2. Giriş Yap: Kayıt olduğunuz kullanıcı adı ve şifre ile giriş yapabilirsiniz.
        
        3. Kitap Ekle: Kitap adı, yazarı, yayınevi ve içeriği bilgilerini doldurarak yeni bir kitap ekleyebilirsiniz.
        
        4. Kitaplar: Eklenen kitapların listesini görebilir ve detaylarına ulaşabilirsiniz.
         """
        messagebox.showinfo("Kullanım Kılavuzu", kullanım_kılavuzu)

class KayitPenceresi(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Kayıt Ol")
        self.geometry("300x200")

        self.label_kullanici_adi = ttk.Label(self, text="Kullanıcı Adı:", font=("Helvetica", 12))
        self.label_kullanici_adi.pack(pady=5)
        self.entry_kullanici_adi = ttk.Entry(self, font=("Helvetica", 12))
        self.entry_kullanici_adi.pack(pady=5)

        self.label_sifre = ttk.Label(self, text="Şifre:", font=("Helvetica", 12))
        self.label_sifre.pack(pady=5)
        self.entry_sifre = ttk.Entry(self, show="*", font=("Helvetica", 12))
        self.entry_sifre.pack(pady=5)

        self.button_kaydet = ttk.Button(self, text="Kaydet", command=self.kaydet)
        self.button_kaydet.pack(pady=5)

    def kaydet(self):
        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()
        if kullanici_adi and sifre:
            with sqlite3.connect("kitaplar.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (kullanici_adi, sifre))
                conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")
            self.destroy()
        else:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve şifre girin.")

class AnaIslemPencere(tk.Tk):
    def __init__(self, kullanici_adi):
        super().__init__()
        self.title("Çevrimiçi Kitap Okuma ve Paylaşım Platformu")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.kullanici_adi = kullanici_adi

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Karanlık tema için 'clam' kullanıyoruz
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TText", font=("Helvetica", 12))

        self.create_widgets()

    def create_widgets(self):
        self.label_baslik = ttk.Label(self, text=f"Merhaba {self.kullanici_adi}", font=("Helvetica", 20, "bold"))
        self.label_baslik.pack(pady=10)

        self.frame_kitaplar = ttk.Frame(self)
        self.frame_kitaplar.pack(pady=20)

        self.listbox_kitaplar = tk.Listbox(self.frame_kitaplar, width=50, height=20, font=("Helvetica", 12))
        self.listbox_kitaplar.grid(row=0, column=0, padx=10, pady=10, rowspan=4)

        self.scrollbar_kitaplar = tk.Scrollbar(self.frame_kitaplar, orient=tk.VERTICAL)
        self.scrollbar_kitaplar.config(command=self.listbox_kitaplar.yview)
        self.scrollbar_kitaplar.grid(row=0, column=1, rowspan=4, sticky='ns')

        self.listbox_kitaplar.config(yscrollcommand=self.scrollbar_kitaplar.set)

        self.button_kitap_ekle = ttk.Button(self, text="Kitap Ekle", command=self.kitap_ekle_pencere_ac)
        self.button_kitap_ekle.pack(pady=10)

        self.kitaplari_goster()

        self.listbox_kitaplar.bind("<<ListboxSelect>>", self.kitap_detayi_goster)

        self.button_cikis = ttk.Button(self, text="Çıkış Yap", command=self.cikis_yap)
        self.button_cikis.place(relx=0.05, rely=0.9)

    def kitaplari_goster(self):
        self.listbox_kitaplar.delete(0, tk.END)
        with sqlite3.connect("kitaplar.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT adi FROM kitaplar")
            kitaplar = cursor.fetchall()
            for kitap in kitaplar:
                self.listbox_kitaplar.insert(tk.END, kitap[0])

    def kitap_detayi_goster(self, event):
        secili_index = self.listbox_kitaplar.curselection()
        if secili_index:
            secili_index = int(secili_index[0])
            secili_kitap_adi = self.listbox_kitaplar.get(secili_index)
            with sqlite3.connect("kitaplar.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM kitaplar WHERE adi=?", (secili_kitap_adi,))
                secili_kitap = cursor.fetchone()
                detay_pencere = tk.Toplevel(self)
                detay_pencere.title(f"{secili_kitap_adi} - Detaylar")
                detay_pencere.geometry("600x400")

                detay_frame = ttk.Frame(detay_pencere)
                detay_frame.pack(pady=10)

                label_detay_baslik = ttk.Label(detay_frame, text="Kitap Detayları", font=("Helvetica", 16, "bold"))
                label_detay_baslik.grid(row=0, column=0, columnspan=2, pady=10)

                label_adi = ttk.Label(detay_frame, text="Kitap Adı:", font=("Helvetica", 12))
                label_adi.grid(row=1, column=0, sticky="e", padx=5, pady=5)
                label_adi_deger = ttk.Label(detay_frame, text=secili_kitap[0], font=("Helvetica", 12))
                label_adi_deger.grid(row=1, column=1, sticky="w", padx=5, pady=5)

                label_yazar = ttk.Label(detay_frame, text="Yazar:", font=("Helvetica", 12))
                label_yazar.grid(row=2, column=0, sticky="e", padx=5, pady=5)
                label_yazar_deger = ttk.Label(detay_frame, text=secili_kitap[1], font=("Helvetica", 12))
                label_yazar_deger.grid(row=2, column=1, sticky="w", padx=5, pady=5)

                label_yayinevi = ttk.Label(detay_frame, text="Yayınevi:", font=("Helvetica", 12))
                label_yayinevi.grid(row=3, column=0, sticky="e", padx=5, pady=5)
                label_yayinevi_deger = ttk.Label(detay_frame, text=secili_kitap[2], font=("Helvetica", 12))
                label_yayinevi_deger.grid(row=3, column=1, sticky="w", padx=5, pady=5)

                button_kitap_oku = ttk.Button(detay_frame, text="Kitabı Oku", command=lambda: self.kitap_oku(secili_kitap[3]))
                button_kitap_oku.grid(row=4, column=0, columnspan=2, pady=10)

                button_yorumlar = ttk.Button(detay_frame, text="Yorumlar", command=lambda: self.yorumlar_goster(secili_kitap_adi))
                button_yorumlar.grid(row=5, column=0, columnspan=2, pady=10)

    def yorumlar_goster(self, kitap_adi):
        yorumlar_pencere = tk.Toplevel(self)
        yorumlar_pencere.title(f"{kitap_adi} - Yorumlar")
        yorumlar_pencere.geometry("600x400")

        frame_yorumlar = ttk.Frame(yorumlar_pencere)
        frame_yorumlar.pack(pady=10)

        label_yorumlar = ttk.Label(frame_yorumlar, text="Yorumlar", font=("Helvetica", 14, "bold"))
        label_yorumlar.grid(row=0, column=0, padx=5, pady=5)

        listbox_yorumlar = tk.Listbox(frame_yorumlar, width=50, height=10, font=("Helvetica", 12))
        listbox_yorumlar.grid(row=1, column=0, padx=5, pady=5)

        scrollbar_yorumlar = tk.Scrollbar(frame_yorumlar, orient=tk.VERTICAL)
        scrollbar_yorumlar.config(command=listbox_yorumlar.yview)
        scrollbar_yorumlar.grid(row=1, column=1, sticky='ns')

        listbox_yorumlar.config(yscrollcommand=scrollbar_yorumlar.set)

        with sqlite3.connect("kitaplar.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT yorum FROM yorumlar WHERE kitap_adi=?", (kitap_adi,))
            yorumlar = cursor.fetchall()
            for yorum in yorumlar:
                listbox_yorumlar.insert(tk.END, yorum[0])

        text_yorum = scrolledtext.ScrolledText(frame_yorumlar, width=50, height=3, font=("Helvetica", 12))
        text_yorum.grid(row=2, column=0, padx=5, pady=5)

        button_yorum_yap = ttk.Button(frame_yorumlar, text="Yorum Yap", command=lambda: self.yorum_yap(kitap_adi, text_yorum))
        button_yorum_yap.grid(row=3, column=0, padx=5, pady=5)

    def yorum_yap(self, kitap_adi, text_yorum):
        yorum = text_yorum.get("1.0", tk.END).strip()
        if yorum:
            with sqlite3.connect("kitaplar.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO yorumlar (kitap_adi, yorum) VALUES (?, ?)", (kitap_adi, yorum))
                conn.commit()
            messagebox.showinfo("Başarılı", "Yorumunuz başarıyla eklendi.")
        else:
            messagebox.showerror("Hata", "Lütfen yorumunuzu girin.")

    def kitap_oku(self, icerik):
        kitap_oku_pencere = tk.Toplevel(self)
        kitap_oku_pencere.title("Kitap Oku")
        kitap_oku_pencere.geometry("800x600")

        text_icerik = scrolledtext.ScrolledText(kitap_oku_pencere, width=100, height=30, font=("Helvetica", 12))
        text_icerik.pack()
        text_icerik.insert(tk.END, icerik)

    def kitap_ekle_pencere_ac(self):
        kitap_ekle_pencere = tk.Toplevel(self)
        kitap_ekle_pencere.title("Kitap Ekle")
        kitap_ekle_pencere.geometry("400x400")

        label_kitap_adi = ttk.Label(kitap_ekle_pencere, text="Kitap Adı:", font=("Helvetica", 12))
        label_kitap_adi.pack()
        entry_kitap_adi = ttk.Entry(kitap_ekle_pencere, font=("Helvetica", 12))
        entry_kitap_adi.pack()

        label_yazar = ttk.Label(kitap_ekle_pencere, text="Yazar:", font=("Helvetica", 12))
        label_yazar.pack()
        entry_yazar = ttk.Entry(kitap_ekle_pencere, font=("Helvetica", 12))
        entry_yazar.pack()

        label_yayinevi = ttk.Label(kitap_ekle_pencere, text="Yayınevi:", font=("Helvetica", 12))
        label_yayinevi.pack()
        entry_yayinevi = ttk.Entry(kitap_ekle_pencere, font=("Helvetica", 12))
        entry_yayinevi.pack()

        label_icerik = ttk.Label(kitap_ekle_pencere, text="İçerik:", font=("Helvetica", 12))
        label_icerik.pack()
        text_icerik = scrolledtext.ScrolledText(kitap_ekle_pencere, width=30, height=10, font=("Helvetica", 12))
        text_icerik.pack()

        button_dosya_sec = ttk.Button(kitap_ekle_pencere, text="Dosya Seç",
                                       command=lambda: self.dosya_sec(text_icerik))
        button_dosya_sec.pack(pady=5)

        button_kitap_ekle = ttk.Button(kitap_ekle_pencere, text="Kitap Ekle",
                                       command=lambda: self.kitap_ekle(entry_kitap_adi.get(), entry_yazar.get(),
                                                                        entry_yayinevi.get(), text_icerik.get(1.0, tk.END)))
        button_kitap_ekle.pack(pady=5)

    def dosya_sec(self, text_icerik):
        dosya_adi = filedialog.askopenfilename(filetypes=[("Text Dosyaları", "*.txt")])
        if dosya_adi:
            with open(dosya_adi, "r", encoding="utf-8") as dosya:
                icerik = dosya.read()
                text_icerik.delete(1.0, tk.END)
                text_icerik.insert(tk.END, icerik)

    def kitap_ekle(self, adi, yazar, yayinevi, icerik):
        if adi and yazar and yayinevi and icerik:
            kitap = Kitap(adi, yazar, yayinevi, icerik)
            kitap.kitap_ekle()
            messagebox.showinfo("Başarılı", "Kitap başarıyla eklendi.")
            self.kitaplari_goster()
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

    def cikis_yap(self):
        self.destroy()
        giris_pencere = AnaPencere()

def veritabani_olustur():
    with sqlite3.connect("kitaplar.db") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kitaplar (adi TEXT, yazar TEXT, yayinevi TEXT, icerik TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS kullanicilar (kullanici_adi TEXT, sifre TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS yorumlar (kitap_adi TEXT, yorum TEXT)")
        cursor.execute("INSERT INTO kullanicilar (kullanici_adi, sifre) VALUES ('admin', '1234')")

if __name__ == "__main__":
    veritabani_olustur()
    app = AnaPencere()
    app.mainloop()
