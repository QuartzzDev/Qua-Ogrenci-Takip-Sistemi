# QuartzzDev

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QDialog, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox

class OgrenciYonetimSistemi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quartzz Öğrenci Yönetim Sistemi")
        self.init_ui()

    def init_ui(self):
        self.ad_label = QLabel("Ad:")
        self.ad_input = QLineEdit()
        self.soyad_label = QLabel("Soyad:")
        self.soyad_input = QLineEdit()
        self.no_label = QLabel("Öğrenci Numarası:")
        self.no_input = QLineEdit()

        self.ekle_button = QPushButton("Ekle")
        self.listele_button = QPushButton("Listele")
        self.ara_button = QPushButton("Ara")
        self.sil_button = QPushButton("Sil")

        self.ogrenciler_combo = QComboBox()  
        self.dersler_combo = QComboBox() 
        self.bilgi_alani = QTextEdit()
        self.bilgi_alani.setReadOnly(True)

        self.ekle_button.clicked.connect(self.ogrenci_ekle)
        self.listele_button.clicked.connect(self.ogrenci_listele)
        self.ara_button.clicked.connect(self.ogrenci_ara)
        self.sil_button.clicked.connect(self.ogrenci_sil)
        self.ogrenciler_combo.currentIndexChanged.connect(self.ogrenci_secildi)  

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ad_label)
        self.layout.addWidget(self.ad_input)
        self.layout.addWidget(self.soyad_label)
        self.layout.addWidget(self.soyad_input)
        self.layout.addWidget(self.no_label)
        self.layout.addWidget(self.no_input)

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.ekle_button)
        self.h_layout.addWidget(self.listele_button)
        self.h_layout.addWidget(self.ara_button)
        self.h_layout.addWidget(self.sil_button)

        self.layout.addWidget(self.ogrenciler_combo)  

        self.dersler_label = QLabel("Ders:")
        self.layout.addWidget(self.dersler_label)
        self.layout.addWidget(self.dersler_combo)  
        self.layout.addLayout(self.h_layout)
        self.layout.addWidget(self.bilgi_alani)

        self.setLayout(self.layout)

        self.ogrenci_tablosu = QTableWidget()
        self.ogrenci_tablosu.setColumnCount(3)
        self.ogrenci_tablosu.setHorizontalHeaderLabels(["Öğrenci Adı", "Ders", "Not"])
        self.ogrenci_tablosu.hide()
        self.ogrenci_tablosu.setFixedSize(400, 200)

        self.not_verme_ekrani_acildi = False

    def ogrenci_ekle(self):
        ad = self.ad_input.text()
        soyad = self.soyad_input.text()
        ogrenci_no = self.no_input.text()

        with open("ogrenciler.txt", "a") as dosya:
            dosya.write(f"{ad},{soyad},{ogrenci_no}\n")

        self.bilgi_alani.append(f"{ad} {soyad} adlı öğrenci başarıyla eklendi.")
        self.ogrenciler_combo.addItem(ad)

        
        self.not_verme_ekrani_acildi = True

    def ogrenci_listele(self):
        self.bilgi_alani.clear()
        self.ogrenciler_combo.clear()

        try:
            with open("ogrenciler.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip()
                    if satir:
                        ad, soyad, ogrenci_no = satir.split(",")
                        self.bilgi_alani.append(f"Ad: {ad}, Soyad: {soyad}, Öğrenci No: {ogrenci_no}")
                        self.ogrenciler_combo.addItem(ad)
        except FileNotFoundError:
            self.bilgi_alani.clear()
            self.bilgi_alani.append("Kayıtlı öğrenci bulunmamaktadır.")

        
        self.not_verme_ekrani_acildi = False

    def ogrenci_ara(self):
        self.bilgi_alani.clear()
        aranan_isim = self.ad_input.text().lower()

        try:
            with open("ogrenciler.txt", "r") as dosya:
                for satir in dosya:
                    ad, soyad, no = satir.strip().split(",")
                    if aranan_isim in ad.lower():
                        self.bilgi_alani.append(f"Ad: {ad}, Soyad: {soyad}, Öğrenci No: {no}")
        except FileNotFoundError:
            self.bilgi_alani.clear()
            self.bilgi_alani.append("Kayıtlı öğrenci bulunmamaktadır.")

    def ogrenci_sil(self):
        ogrenci_no = self.no_input.text()
        self.bilgi_alani.clear()

        with open("ogrenciler.txt", "r") as dosya:
            satirlar = dosya.readlines()

        with open("ogrenciler.txt", "w") as dosya:
            for satir in satirlar:
                ad, soyad, no = satir.strip().split(",")
                if no != ogrenci_no:
                    dosya.write(satir)
                else:
                    self.bilgi_alani.append(f"Öğrenci numarası {ogrenci_no} olan öğrenci başarıyla silindi.")
                    self.ogrenciler_combo.removeItem(self.ogrenciler_combo.findText(ad))

    def ogrenci_secildi(self):
        ad = self.ogrenciler_combo.currentText()
        self.bilgi_alani.clear()

        if self.not_verme_ekrani_acildi:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"{ad} - Not Ver")
            dialog.setFixedSize(250, 150)

            label = QLabel("Ders Seç:")
            self.dersler_combo.clear()
            self.dersler_combo.addItems(["Matematik", "Fizik", "Kimya", "Biyoloji", "Türkçe", "Tarih"])

            not_label = QLabel("Not Gir:")
            not_input = QLineEdit()

            def kaydet():
                ders = self.dersler_combo.currentText()
                notu = not_input.text()
                self.notu_kaydet(ad, ders, notu)
                dialog.accept()

            kaydet_button = QPushButton("Kaydet")
            kaydet_button.clicked.connect(kaydet)

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(self.dersler_combo)
            layout.addWidget(not_label)
            layout.addWidget(not_input)
            layout.addWidget(kaydet_button)

            dialog.setLayout(layout)
            dialog.exec_()

            
            self.not_verme_ekrani_acildi = False

    def notu_kaydet(self, ad, ders, notu):
        with open("notlar.txt", "a+") as dosya:
            dosya.seek(0)
            for satir in dosya:
                mevcut_ad, mevcut_ders, mevcut_notu = satir.strip().split(",")
                if mevcut_ad == ad and mevcut_ders == ders:
                    dosya.seek(dosya.tell() - len(satir))
                    dosya.write(f"{ad},{ders},{notu}\n")
                    self.bilgi_alani.append(f"{ad} adlı öğrenciye {ders} dersinden not {notu} olarak güncellendi.")
                    return

            dosya.write(f"{ad},{ders},{notu}\n")
            self.bilgi_alani.append(f"{ad} adlı öğrenciye {ders} dersinden not {notu} olarak eklendi.")

    def ogrenci_notlarini_listele(self):
        self.ogrenci_tablosu.clearContents()
        self.ogrenci_tablosu.setRowCount(0)

        with open("notlar.txt", "r") as dosya:
            for satir in dosya:
                ad, ders, notu = satir.strip().split(",")
                row_count = self.ogrenci_tablosu.rowCount()
                self.ogrenci_tablosu.insertRow(row_count)
                self.ogrenci_tablosu.setItem(row_count, 0, QTableWidgetItem(ad))
                self.ogrenci_tablosu.setItem(row_count, 1, QTableWidgetItem(ders))
                self.ogrenci_tablosu.setItem(row_count, 2, QTableWidgetItem(notu))

    def show_ogrenci_notlar(self):
        self.ogrenci_tablosu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OgrenciYonetimSistemi()
    window.show()
    sys.exit(app.exec_())
