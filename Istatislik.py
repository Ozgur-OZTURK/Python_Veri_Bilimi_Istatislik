#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 13:40:41 2019

@author: Özgür ÖZTÜRK
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.stats.api as sms
from matplotlib.pyplot import plot
from scipy.stats import shapiro
from scipy.stats import levene
from statsmodels.stats.descriptivestats import sign_test
from statsmodels.stats.proportion import proportions_ztest
import seaborn as sns
from scipy.stats import f_oneway
from scipy.stats import kruskal
import seaborn as sns
from scipy.stats.stats import pearsonr


class Istatislik:
    def __init__(self):
      np.random.seed(5)
      self.main_array = np.random.randint(0,300,10000)
      np.random.seed(5)
      self.choice_array = np.random.choice(a = self.main_array, size = 100)
      self.choice_array2 = np.random.choice(a = self.main_array, size = 100)
      self.choice_array3 = np.random.choice(a = self.main_array, size = 100)
    
    def array_mean(self):
        return self.choice_array.mean()
    
    
      # Güven aralıklarını buluyoruz
    def guven_araligi(self):        
        return sms.DescrStatsW(self.choice_array).tconfint_mean()
    
    
    def binom(self):  
        
        bd1 = stats.binom(30, 0.6)
        bd2 = stats.binom(40, 0.3)
        bd3 = stats.binom(25, 0.5)
        
        k = np.arange(50)
        
        plot(k, bd1.pmf(k), 'o-b')
        plot(k, bd2.pmf(k), 'd-r')
        plot(k, bd3.pmf(k), 's-g')        
        
        p=float(input("\n p= Lütfen olasılık degerini giriniz(exp:0.6)"))
        n=int(input("\n n= Lütfen deneme degerini giriniz(exp:50)"))
        k=int(input("\n k= Lütfen hangi degerin karsilikk geldigi degeri bulmak istediginizi yaziniz giriniz(exp:15)"))  
        print("Default Binom Grafigi Gösterildi")
        # 50 deneme sayısında 0.6 olasılıkta 15 değerinin karşılık geldiği olasılığı bulmaktayız
        #p = 0.5
        #n = 40
        rv = stats.binom(n,p)
        return rv.pmf(int(k)) 
    
    
    #Problem: Web sitemizde geçirilen ortalama süre gerçekten beklenen_deger saniye mi?
    def tek_orneklem_t_testi_main(self):
        #H0 hipotezi = Geçirilen süre beklenen_deger'dir.
        #H1 hipotezi = Geçirilen süre beklenen_deger değildir.
        
        #web sitemizde geçirilen, beklenen değer
        beklenen_deger = int(input("Web sitemizde gecirildigini tahmin ettigiz süreyi giriniz"))        
        
        # Tek Örneklem T testi yapabilmemiz için değerler(choice_array = random oluşturulan değer kesitinden aldık) normal dağılıma sahip mi ona bakmalıyız.
        result = Istatislik.shapiro_wilks(self,self.choice_array)
        if result == 0:
            nonparametrik_result = Istatislik.nonparametrik_tek_orneklem_testi(self,beklenen_deger)
            if nonparametrik_result < 0.05:
                return "Web sitesinde geçirilen ortalama süre ="+ str(nonparametrik_result) +" (P_value degeri ) " + str(beklenen_deger) + " değildir "
            else:
                return "Web sitesinde geçirilen ortalama süre ="+ str(nonparametrik_result) +"(P_value degeri ) " + str(beklenen_deger) + " arasında anlamlı düzeyde farklı değildir "
        else:
            tek_orneklem_result =  Istatislik.tek_orneklem_t_testi(self,beklenen_deger)
            if tek_orneklem_result < 0.05:
                return "Web sitesinde geçirilen ortalama süre ="+ str(tek_orneklem_result) +" " + str(beklenen_deger) + " değildir "
            else:
                return "Web sitesinde geçirilen ortalama süre ="+ str(tek_orneklem_result) +" " + str(beklenen_deger) + " arasında anlamlı düzeyde farklı değildir "

    
    def tek_orneklem_t_testi(self,beklenen_deger):
        return float(stats.ttest_1samp(self.choice_array, popmean=beklenen_deger).pvalue)
        
        
    # Dağılımının oarametrik olmadığını biliyoruz çünkü varsayım sağlanmadı    
    def nonparametrik_tek_orneklem_testi(self,beklenen_deger):
        return float(sign_test(self.choice_array,beklenen_deger)[1])
    
    
    #Normallik varsayımı testini yapmak için shapiro_wilks testini kullanmalıyız
    #H0 hipotezi = Verilerde çarpıklık yoktur normal dağılımdır./Teorik dağılım ile örnek dağılım arasında fark olmadığını idda eder
    #H1 hipotezi = Verilerde çarpıklık vardır normal dağılım değildir./Teorik dağılım ile örnek dağılım arasında fark olduğunu idda eder
    def shapiro_wilks(self,py_array):
        
        t_istatislik = float(shapiro(py_array)[0])
        p_value = float(shapiro(py_array)[1])
      
        if p_value < 0.05:
            #H0 hipotezi red edilir
            print("P_value değeri = "+ str(p_value) +" küçük çıktı HO hipotezi(Verilerde çarpıklık yoktur normal dağılımdır) reddedilir.")
            return 0
        else:
            print("P_value değeri = "+ str(p_value) +" büyük çıktı HO hipotezi(Verilerde çarpıklık yoktur normal dağılımdır) reddedilmez.")
            return 1
        
        
    #Varyans homejenlik testini yapmak için levene testini kullanmalıyız
    #H0 hipotezi = Verilerin varyansları homejendir.
    #H1 hipotezi = Verilerin varyansları homejen değildir.
    def levene(self,A_B):
        p_value = float(levene(A_B.A,A_B.B)[1])
        
        if p_value < 0.05:
        #H0 hipotezi red edilir
            print("P_value değeri = "+ str(p_value) +" küçük çıktı HO hipotezi(Verilerin varyansları homejendir) reddedilir.")
            return 0
        else:
            print("P_value değeri = "+ str(p_value) +" büyük çıktı HO hipotezi(Verilerin varyansları homejendir) reddedilmez.")
            return 1
        
        
    
    #Web sitemize gelen dönüşüm oranı test edilmek isteniyor
    #HO hipotezi = 0,04 oranında web sitemizde dönüşüm vardır(farklılık yoktur ilk degerle)
    #H1 hipotezi = 0,04 oranında web sitemizde dönüşüm yoktur(farklılık vardır ilk degerle).
    #1000 kişi tıklamış 25 tanesi yorum yapmış diyelim / oranımız=0,025 => Yorum yapanlar / Websitemize giren
    def tek_orneklem_oran_testi(self):
        count = int(input("Gözlenmiş başarı sayısı(exp=25) kişi yorum yaptı"))
        nobs = stats.describe(self.choice_array).nobs #gözlem sayısı
        value = 0.04 # sınanacak olan null hipotezimizin değeri
        p_value = float(proportions_ztest(count, nobs, value)[1])
        
        if p_value<0.05:
            #HO hipoteti red edilir
            return "(P_value="+str(p_value)+") 0.04 oranında web sitemize dönüşüm yoktur(Verilen ilk degerle aralarında farklılık var demektir)"
        else:
            return "(P_value="+str(p_value)+") 0.04 oranında web sitemize dönüş vardır(Verilen ilk degerle aralarında farklılık yok demektir)"
        
        
    #Hikayemiz: Firmamıza kurulan yeni sistem ile eski sistem arasında anlamlı derece bir farklılığımız var mı ona bakıyoruz
    #HO = Eski sistem ve yeni sistem arasında anlamlı derecede bir farklılık yoktur.
    #H1 = Eski sistem ve yeni sistem arasında anlamlı derecede bir farklılık vardır.
    def bagimsiz_iki_orneklem_t_testi(self):
        A = pd.DataFrame(self.choice_array)
        B = pd.DataFrame(self.choice_array2)
        # A ve B verilerini yanyana birleştirelim
        A_B = pd.concat([A,B], axis = 1)
        A_B.columns = ["A","B"]

        
        # A ve B verilerini şimdi alt alta gruplayarak birleştireli        
        Grup_A = pd.DataFrame(A)
        Grup_A_copy = Grup_A.copy()
        Grup_A_copy[:] = "A"
        A = pd.concat([Grup_A, Grup_A_copy], axis = 1)
        
        Grup_B = pd.DataFrame(B)
        Grup_B_copy = Grup_B.copy()
        Grup_B_copy[:] = "B"
        B = pd.concat([Grup_B, Grup_B_copy], axis = 1)
        
        AB = pd.concat([A,B])
        AB.columns = ["Bilgi","Grup"]   
        
        # Belli bir veriden örnekleme aldığımızdan, örneklemelerin varsayım kontrollerini yapmamız lazım
        # - normallik varsayımı(shapiro)
        # - varyans homejenlik varsayımı(levene)
        shapiro_result = int(Istatislik.shapiro_wilks(self,self.choice_array))
        levene_result = int(Istatislik.levene(self,A_B))
        
        if (shapiro_result == 1) and (levene_result == 1):
            # Verilerde çarpıklık yoktur normal dağılımdır
            # Verilerin varyansları homejendir.
            #equal_var =True varyans homejen testimizi yaptık demektir.
            bagimsiz_iki_orneklem_t_testi_result = float(stats.ttest_ind(A_B["A"], A_B["B"], equal_var = True).pvalue)
            
            if bagimsiz_iki_orneklem_t_testi_result < 0.05:    
                return "P_value değeri= " + str(bagimsiz_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Eski sistem ve Yeni sistem arasında anlamlı derecede bir farklılık yoktur) red edilir "
            else:
               return "P_value değeri= " + str(bagimsiz_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Eski sistem ve Yeni sistem arasında anlamlı derecede bir farklılık yoktur) kabul edilir"
        else:
            # Varsayımlar sağlanmadığı için Non Parametrik Bağımsız İki Örneklem T Testi
            non_parametrik_bagimsiz_iki_orneklem_t_testi_result = Istatislik.non_parametrik_bagimsiz_iki_orneklem_t_testi(self,A_B)
            if non_parametrik_bagimsiz_iki_orneklem_t_testi_result < 0.05:
                return "P_value değeri= " + str(non_parametrik_bagimsiz_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Eski sistem ve Yeni sistem arasında anlamlı derecede bir farklılık yoktur) red edilir "
            else:
               return "P_value değeri= " + str(non_parametrik_bagimsiz_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Eski sistem ve Yeni sistem arasında anlamlı derecede bir farklılık yoktur) kabul edilir"
            
            
           
    # Bağımsız iki örneklemde eğer varsayımlar sağlanmamışsa Non Parametrik Bağımsız İki Örneklem T Testini yaparız
    # Non Parametrik Bağımsız İki Örneklem T Testi    
    def non_parametrik_bagimsiz_iki_orneklem_t_testi(self,A_B):
        return float(stats.mannwhitneyu(A_B["A"], A_B["B"]).pvalue)
    #-------------------------------------------------------------------------------------    

    #Hikayemiz: Firmamızın personeline ait farklı dönemlerdeki satışlar
    #HO = Dönemler arasında anlamlı derecede bir farklılık yoktur.
    #H1 = Dönemler arasında anlamlı derecede bir farklılık vardır.
    def bagimli_iki_orneklem_t_testi(self):
        A = pd.DataFrame(self.choice_array)
        B = pd.DataFrame(self.choice_array2)
        # A ve B verilerini yanyana birleştirelim
        A_B = pd.concat([A,B], axis = 1)
        A_B.columns = ["A","B"]

        
        # A ve B verilerini şimdi alt alta gruplayarak birleştirelim       
        Grup_A = pd.DataFrame(A)
        Grup_A_copy = Grup_A.copy()
        Grup_A_copy[:] = "A"
        A = pd.concat([Grup_A, Grup_A_copy], axis = 1)
        
        Grup_B = pd.DataFrame(B)
        Grup_B_copy = Grup_B.copy()
        Grup_B_copy[:] = "B"
        B = pd.concat([Grup_B, Grup_B_copy], axis = 1)
        
        AB = pd.concat([A,B])
        AB.columns = ["Satis","Grup"]   
        
        # Belli bir veriden örnekleme aldığımızdan, örneklemelerin varsayım kontrollerini yapmamız lazım
        # - normallik varsayımı(shapiro)
        # - varyans homejenlik varsayımı(levene)
        shapiro_result = int(Istatislik.shapiro_wilks(self,self.choice_array))
        levene_result = int(Istatislik.levene(self,A_B))
        
        if (shapiro_result == 1) and (levene_result == 1):
            # Verilerde çarpıklık yoktur normal dağılımdır
            # Verilerin varyansları homejendir.
            bagimli_iki_orneklem_t_testi_result = float(stats.ttest_rel(A_B["A"], A_B["B"]).pvalue)
            
            if bagimli_iki_orneklem_t_testi_result < 0.05:    
                return "P_value değeri= " + str(bagimli_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Dönemler arasında anlamlı derecede bir farklılık yoktur) red edilir "
            else:
               return "P_value değeri= " + str(bagimli_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Dönemler arasında anlamlı derecede bir farklılık yoktur) kabul edilir"
        else:
            # Varsayımlar sağlanmadığı için Non Parametrik Bağımsız İki Örneklem T Testi
            non_parametrik_bagimli_iki_orneklem_t_testi_result = Istatislik.non_parametrik_bagimli_iki_orneklem_t_testi(self,A_B)
            if non_parametrik_bagimli_iki_orneklem_t_testi_result < 0.05:
                return "P_value değeri= " + str(non_parametrik_bagimli_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Dönemler arasında anlamlı derecede bir farklılık yoktur) red edilir "
            else:
               return "P_value değeri= " + str(non_parametrik_bagimli_iki_orneklem_t_testi_result) + " olduğundan dolayı HO hipotezi(Dönemler arasında anlamlı derecede bir farklılık yoktur) kabul edilir"
                        
           
    # Bağımlı iki örneklemde eğer varsayımlar sağlanmamışsa Non Parametrik Bağımlı İki Örneklem T Testini yaparız
    # Non Parametrik Bağımsız İki Örneklem T Testi    
    def non_parametrik_bagimli_iki_orneklem_t_testi(self,A_B):
        return float(stats.wilcoxon(A_B["A"], A_B["B"]).pvalue)
    
    
    # İki Örneklem Oran Testi
    # Hikayemiz = A ayakkabısının bulunduğu sayfa 1700 kere görüntülenmiş 500 kere ise ayakkabı detayına bakılmış
    #          B ayakkabısının bulunduğu sayfa 1800 kere görüntülenmiş 600 kere ise ayakkabı detayına bakılmış
    # HO hipotezi = İki oran arasında anlamlı bir farklılık yoktur
    # H1 hipotezi = İki oran arasında anlamlı bir farklılık vardır
    def iki_orneklem_oran_testi(self):
        detaya_bakilma_sayisi = np.array([500,600])
        goruntulenme_sayisi = np.array([1700,1800])
        
        iki_orneklem_oran_testi_result = float(proportions_ztest(detaya_bakilma_sayisi,goruntulenme_sayisi)[1])
        
        if iki_orneklem_oran_testi_result < 0.05:    
                return "P_value değeri= " + str(iki_orneklem_oran_testi_result) + " olduğundan dolayı HO hipotezi(İki oran arasında anlamlı bir farklılık yoktur) red edilir "
        else:
               return "P_value değeri= " + str(iki_orneklem_oran_testi_result) + " olduğundan dolayı HO hipotezi(İki oran arasında anlamlı bir farklılık yoktur) kabul edilir"

    
    # Varyans Analizi üç ve üçten fazla grubun karşılaştırılmasında kullanılır 
    # Hikayemiz = Bir e-ticaret web sitemiz var ve biz bir birinden farklı ayakkabı bölümleri yaptık daha sonra kullanıcılarımızın web sayfamızda geçirdiği süreleri 3 gruba ayırdık ve bu gruplar arasında anlamlı bir farklılık var mı ona bakmak istiyoruz
    # H0 hipotezimiz = 3 grup arasında anlamlı bir farklılık yoktur
    # H1 hipotezimiz = 3 grup arasında anlamlı bir farklılık vardır
    def varyans_analizi(self):
        
        spor_ayakkabi = pd.DataFrame(self.choice_array)
        kosu_ayakkabi = pd.DataFrame(self.choice_array2)
        kislik_ayakkabi = pd.DataFrame(self.choice_array3)
        
        ayakkabi = pd.concat([spor_ayakkabi,kosu_ayakkabi,kislik_ayakkabi], axis = 1)
        ayakkabi.columns = ["spor","kosu","kislik"]
        
        spor_shapiro = Istatislik.shapiro_wilks(self,ayakkabi['spor'])
        kosu_shapiro = Istatislik.shapiro_wilks(self,ayakkabi['kosu'])
        kislik_shapiro = Istatislik.shapiro_wilks(self,ayakkabi['kislik'])
        
        ayakkabi_levene = float(stats.levene(ayakkabi['spor'],ayakkabi['kosu'],ayakkabi['kislik']).pvalue)
        if ayakkabi_levene < 0.05:
        #H0 hipotezi red edilir
            print("P_value değeri = "+ str(ayakkabi_levene) +" küçük çıktı HO hipotezi(Verilerin varyansları homejendir) reddedilir.")
            ayakkabi_levene = 0
        else:
            print("P_value değeri = "+ str(ayakkabi_levene) +" büyük çıktı HO hipotezi(Verilerin varyansları homejendir) reddedilmez.")
            ayakkabi_levene = 1            
            
        
        if (spor_shapiro == 1 ) and (kosu_shapiro == 1 ) and (kislik_shapiro == 1 ) and (ayakkabi_levene == 1):
	    #p_value değeri küçüldükçe anlamlı fark artar 0.05 alırsak %95 güven aralığı 0.01 alırsak %99 güven aralığı deriz
            varyans_analizi_result = float(f_oneway(ayakkabi['spor'],ayakkabi['kosu'],ayakkabi['kislik']).pvalue)
            if varyans_analizi_result < 0.05:
                return "P_value değeri= " + str(varyans_analizi_result) + " olduğundan dolayı HO hipotezi(Üç oran arasında anlamlı bir farklılık yoktur) red edilir "
            else:
                return "P_value değeri= " + str(varyans_analizi_result) + " olduğundan dolayı HO hipotezi(Üç oran arasında anlamlı bir farklılık yoktur) kabul edilir "
        else:
             # Varsayımlar sağlanmadığı için Non Parametrik Varyans Analisi Testi
            non_parametrik_varyans_analizi_result = Istatislik.non_parametrik_varyans_analizi(self,ayakkabi)
            if non_parametrik_varyans_analizi_result < 0.05:
                return "P_value değeri= " + str(non_parametrik_varyans_analizi_result) + " olduğundan dolayı HO hipotezi(Üç oran arasında anlamlı bir farklılık yoktur) red edilir "
            else:
               return "P_value değeri= " + str(non_parametrik_varyans_analizi_result) + " olduğundan dolayı HO hipotezi(Üç oran arasında anlamlı bir farklılık yoktur)  kabul edilir"
            
     
    # H0 hipotezimiz = 3 grup arasında anlamlı bir farklılık yoktur
    # H1 hipotezimiz = 3 grup arasında anlamlı bir farklılık vardır          
    def non_parametrik_varyans_analizi(self,ayakkabi):
        return float(kruskal(ayakkabi['spor'],ayakkabi['kosu'],ayakkabi['kislik']).pvalue)
    
    
    # Korelasyon analizi
    # Değişkenler arasında ilişki varmı hangi yöndedir diye bakmak istersek kullanacağımız analizdir
    # HO Değişkenler arasında anlamlı farklılık yoktur.
    # H1 Değişkenler arasında anlamlı farklılık vardır.
    def korelasyon_analizi(self):
        bahsis_data_set = sns.load_dataset('tips')
        
        #grafik çizerek korelasyonun yönün ve kuvvetini gözlemleyebiliriz
        sns.jointplot(x = "total_bill", y ="tip", data = bahsis_data_set, kind ="reg")
        
        # Varsayım normallik testi yapmalıyız
        bahsis_shapiro = Istatislik.shapiro_wilks(self,bahsis_data_set['tip'])
        ucret_shapiro = Istatislik.shapiro_wilks(self,bahsis_data_set['total_bill'])
        
        if (bahsis_shapiro == 1) and (ucret_shapiro == 1):
            # varsayımlar sağlandığı için korelasyon_analizine devam edebiliriz
            # Korelasyon katsayısı 1′ e yaklaştıkça değişkenler arasındaki ilişkinin yükseldiğini, 
            # Korelasyon katsayısı 0’a yaklaştıkça değişkenler arasındaki ilişkinin azaldığını görebiliriz.
            # Korelasyon 1 olduğunda ilişki mükemmel, 0 olduğunda ise ilişki yok demektir.
            korelasyon_katsayisi = float(bahsis_data_set['tip'].corr(bahsis_data_set['total_bill']))
            if korelasyon_katsayisi <= 0.2:
                print("Korelasyon Katsayısı= " + str(korelasyon_katsayisi) + " 0.2 den küçük olduğundan değişkenler arasında çok zayıf düzeyde ilişki vardır.")
            elif (korelasyon_katsayisi > 0.2) and korelasyon_katsayisi <= 0.39:
                print("Korelasyon Katsayısı= " + str(korelasyon_katsayisi) + " 0.2-0.39 arası olduğundan değişkenler arasında zayıf düzeyde ilişki vardır.")
            elif (korelasyon_katsayisi > 0.39) and korelasyon_katsayisi <= 0.59:
                print("Korelasyon Katsayısı= " + str(korelasyon_katsayisi) + " 0.39-0.59 arası olduğundan değişkenler arasında orta düzeyde ilişki vardır.")
            elif (korelasyon_katsayisi > 0.59) and korelasyon_katsayisi <= 0.79:
                print("Korelasyon Katsayısı= " + str(korelasyon_katsayisi) + " 0.59-0.79 arası olduğundan değişkenler arasında yüksek düzeyde ilişki vardır.")
            elif (korelasyon_katsayisi > 0.79) and korelasyon_katsayisi <= 1.0:
                print("Korelasyon Katsayısı= " + str(korelasyon_katsayisi) + " 0.79-1.0 arası olduğundan değişkenler arasında çok yüksek düzeyde ilişki vardır.")
            
            korelasyon_analizi_result = float(pearsonr(bahsis_data_set['total_bill'],bahsis_data_set['tip'])[1])
            if korelasyon_analizi_result < 0.0:
                return "P_value değeri= " + str(korelasyon_analizi_result) + " olduğundan dolayı değişkenler arasında negatif yönde ilişki vardır"
            else:
                return "P_value değeri= " + str(korelasyon_analizi_result) + " olduğundan dolayı değişkenler arasında pozitif yönde ilişki vardır "
        else:
            #varsayımlar sağlanmadığı için non_parametrik_korelasyon_analizine devam edebiliriz
            non_parametrik_korelasyon_testi_result_p_value = float(Istatislik.non_parametrik_korelasyon_testi(self,bahsis_data_set).pvalue)
            non_parametrik_korelasyon_testi_result_korelasyon_katsayisi = float(Istatislik.non_parametrik_korelasyon_testi(self,bahsis_data_set).correlation)
            
            if non_parametrik_korelasyon_testi_result_korelasyon_katsayisi <= 0.2:
                return "Non Parametrik Korelasyon Katsayısı= " + str(non_parametrik_korelasyon_testi_result_korelasyon_katsayisi) + " 0.2 den küçük olduğundan değişkenler arasında çok zayıf düzeyde ilişki vardır."
            elif (non_parametrik_korelasyon_testi_result_korelasyon_katsayisi > 0.2) and non_parametrik_korelasyon_testi_result_korelasyon_katsayisi <= 0.39:
                return "Non Parametrik Korelasyon Katsayısı= " + str(non_parametrik_korelasyon_testi_result_korelasyon_katsayisi) + " 0.2-0.39 arası olduğundan değişkenler arasında zayıf düzeyde ilişki vardır."
            elif (non_parametrik_korelasyon_testi_result_korelasyon_katsayisi > 0.39) and non_parametrik_korelasyon_testi_result_korelasyon_katsayisi <= 0.59:
                return "Non Parametrik Korelasyon Katsayısı= " + str(non_parametrik_korelasyon_testi_result_korelasyon_katsayisi) + " 0.39-0.59 arası olduğundan değişkenler arasında orta düzeyde ilişki vardır."
            elif (non_parametrik_korelasyon_testi_result_korelasyon_katsayisi > 0.59) and non_parametrik_korelasyon_testi_result_korelasyon_katsayisi <= 0.79:
                return "Non Parametrik Korelasyon Katsayısı= " + str(non_parametrik_korelasyon_testi_result_korelasyon_katsayisi) + " 0.59-0.79 arası olduğundan değişkenler arasında yüksek düzeyde ilişki vardır."
            elif (non_parametrik_korelasyon_testi_result_korelasyon_katsayisi > 0.79) and non_parametrik_korelasyon_testi_result_korelasyon_katsayisi <= 1.0:
                return "Non Parametrik Korelasyon Katsayısı= " + str(non_parametrik_korelasyon_testi_result_korelasyon_katsayisi) + " 0.79-1.0 arası olduğundan değişkenler arasında çok yüksek düzeyde ilişki vardır."            
  
  
    # varsayımlar sağlanmadığı için Non Parametrik Korelasyon Testi yapılır   
    def non_parametrik_korelasyon_testi(self,bahsis_data_set):
        return stats.spearmanr(bahsis_data_set['total_bill'],bahsis_data_set['tip'])
        

        
        
        
        
        
        

        
        
