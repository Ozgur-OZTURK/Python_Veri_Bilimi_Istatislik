#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:38:29 2019

@author: wasp
"""



import Istatislik
class_istatislik = Istatislik.Istatislik()

numara = input(" 1- ORTALAMASI \n 2- GUVEN ARALIGI \n 3- BINOM DAGILIMI \n 4- TEK ORNEKLEM TESTI \n 5- TEK ORNEKLEM ORAN TESTI \n 6- BAGIMSIZ IKI ORNEKLEM T TESTI \n 7- BAGIMLI IKI ORNEKLEM T TESTI \n 8- IKI ORNEKLEM ORAN TESTI \n 9- VARYANS ANALIZI \n 10- KORELASYON ANALIZI \n LUTFEN YAPMAK ISTEDIGINIZ ISLEMİN NUMARASINI YAZINIZ ")

if numara == "1":
    print("\n Dizinin Ortalaması = ", class_istatislik.array_mean())
elif numara == "2":
    print("\n Dizinin Guven Araligi = ", class_istatislik.guven_araligi())
elif numara == "3":
    print("\n Sonuc= n Deneme Sayısında p Olasılıkta k Değerinin Karşılık Geldiği Olasılığı Bulmaktayız", class_istatislik.binom())
elif numara == "4":
    print("\n Sonuc=", class_istatislik.tek_orneklem_t_testi_main())
elif numara == "5":
    print("\n Sonuc=", class_istatislik.tek_orneklem_oran_testi())
elif numara == "6":
    print("\n Sonuc=", class_istatislik.bagimsiz_iki_orneklem_t_testi())
elif numara == "7":
    print("\n Sonuc=", class_istatislik.bagimli_iki_orneklem_t_testi())
elif numara == "8":
    print("\n Sonuc=", class_istatislik.iki_orneklem_oran_testi())
elif numara == "9":
    print("\n Sonuc=", class_istatislik.varyans_analizi())
elif numara == "10":
    print("\n Sonuc=", class_istatislik.korelasyon_analizi())


