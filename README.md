# real-time-lane-tracking-system!

[Screenshot from 2025-06-15 18-09-34](https://github.com/user-attachments/assets/03fd11d7-7574-4b44-b27b-bf6cf8a60ae0)


Özet
Otonom sürüş ve gelişmiş sürücü destek sistemlerinde şerit takip sistemleri hayati bir rol oynamaktadır.
Birçok trafik kazası, aracın istem dışı şeritten ayrılması nedeniyle meydana geldiğinden, araçların şerit
içinde kalmasını sağlayan sistemler hem yolcu güvenliği hem de trafikteki diğer araçların güvenliği için
kritiktir. Bu projede, ROS2 altyapısı ve Webots simülasyon ortamı kullanılarak Python ile OpenCV tabanlı
geleneksel görüntü işleme yöntemleriyle bir şerit takip sistemi gerçekleştirilmiştir. Gerçek zamanlı
simülasyon verisi olarak araç üzerindeki kameradan alınan görüntüler işlenerek aracın yoldaki şerit
çizgilerini algılaması ve şerit içinde kalacak şekilde direksiyon kontrolü sağlanmıştır. Materyal ve metot
bölümünde kullanılan donanım/simülasyon bileşenleri, ROS2 ve Webots entegrasyonu ile görüntü işleme
algoritmasının adımları detaylı olarak açıklanmaktadır. Simülasyon verisi bölümünde Webots ortamında
araç kamerasından alınan gerçek zamanlı görüntülerin nasıl işlendiği anlatılmaktadır. Deneysel sonuçlar
bölümünde, sistemin Webots üzerindeki gözlemsel başarımı nitel olarak değerlendirilmiş ve aracın şerit
takip yeteneği ortaya konmuştur. Son olarak tartışma bölümünde, kullanılan geleneksel (kural tabanlı)
görüntü işleme yaklaşımı ile derin öğrenme tabanlı şerit tespit yöntemleri karşılaştırılarak avantaj ve
dezavantajları üzerinde durulmuştur.
Abstract
Lane keeping systems play a crucial role in autonomous driving and advanced driver assistance systems.
Since many traffic accidents occur due to unintentional lane departures, systems that keep vehicles centered
in their lane are critical for both passenger safety and the safety of other road users. In this project, a lane
following system has been implemented using traditional image processing methods with OpenCV in
Python, leveraging a ROS2 framework and the Webots simulation environment. Real-time simulation data
from an on-vehicle camera is processed to detect lane markings on the road and steer the vehicle to remain
within its lane. In the Materials and Methods, we detail the hardware/simulation components used, the
integration of ROS2 with Webots, and the step-by-step image processing algorithm. The Simulation Data
section explains how real-time images from the Webots vehicle camera are processed. The Experimental
Results section qualitatively evaluates the observed performance of the system in Webots, demonstrating
the vehicle’s ability to follow the lane. Finally, the Discussion compares the traditional (rule-based) image
processing approach used with deep learning-based lane detection methods, highlighting their respective
advantages and disadvantages.
Giriş
Şerit takip sistemleri, modern otomotiv güvenlik teknolojilerinin ve otonom araç kontrolünün önemli bir
parçasıdır. Bu sistemler, aracın şerit çizgilerini algılayarak sürücünün istem dışı şerit dışına çıkmasını
engeller ve böylece olası kazaların önüne geçer. Özellikle uzun yolculuklarda veya otoyol sürüşünde, şerit
takip asistanı sürücüye sesli veya görsel uyarılar vererek ya da doğrudan direksiyon kontrolüne müdahale
ederek aracı şeritte tutmaya yardımcı olur. Gelişmiş Sürücü Destek Sistemleri (ADAS) ve otonom araçlar,
şerit algılama ve takip yeteneklerine büyük ölçüde dayanırlar; aracın şeritten ayrılması durumunda uyarı
verilmesi veya aracı tekrar merkeze alma gibi işlevler sürüş güvenliğini önemli ölçüde artırır.Şerit takip sistemlerinin önemi sadece otomotiv sektöründe değil, aynı zamanda robotik uygulamalarda da
kendini gösterir. Örneğin, depolarda veya üretim hatlarında zemine çizilmiş çizgileri takip eden otonom
mobil robotlar, rotalarını bu çizgilere göre ayarlayarak güvenli ve verimli bir şekilde hareket edebilirler.
Benzer şekilde, robotik yarışmalar veya eğitim projelerinde de çizgi izleyen robot uygulamaları yaygındır.
Bu proje kapsamında ise bir kara yolu senaryosunda aracın şeritleri takip etmesi ele alınmıştır.
Projenin Amacı: ROS2, Webots ve OpenCV kullanarak gerçek zamanlı bir şerit tespit ve takip sistemi
geliştirmektir. Bu amaçla, Webots simülasyon ortamında bir araç modeli ve yol senaryosu oluşturulmuş;
aracın üzerine yerleştirilen bir kamera yardımıyla yol üzerindeki şerit çizgileri algılanmıştır. ROS2 altyapısı
sayesinde kamera tarafından elde edilen görüntüler, bir görüntü işleme düğümü tarafından abonelik
mekanizması ile alınarak işlenmiş ve sonucunda hesaplanan direksiyon komutları araca iletilmiştir. Bu
sayede araç, şerit merkezi referans alınarak sürekli olarak direksiyonunu ayarlamakta ve şerit içerisinde
kalmaktadır. Proje, gerçek dünyadaki otonom sürüş algoritmalarının bir prototipi olup, geleneksel görüntü
işleme tekniklerinin bu alandaki etkinliğini demonstratif olarak ortaya koymayı hedeflemektedir.
Materyal ve Metot
Kullanılan Platformlar ve Araçlar
Webots Simülasyon Ortamı: Webots, robotik sistemleri ve sensörlerini gerçekçi bir şekilde
modelleyebilen, fizik motoru içeren bir açık kaynaklı simülatördür. Bu projede Webots üzerinde bir araba
modeli ve yol ortamı oluşturulmuştur. Yol üzerinde belirgin şerit çizgileri bulunmaktadır (örneğin sarı veya
beyaz renkli şeritler). Araç modelinin ön kısmında veya tavanında yol kamerasını temsil eden bir kamera
sensörü yer alır. Bu kamera, belirli bir çözünürlükte (örneğin 640×480 piksel) ve kare hızında gerçek
zamanlı görüntü akışı sağlamaktadır. Webots'un Camera nesnesi, kontrol yazılımı tarafından her zaman
adımında görüntü alınabilmesine olanak tanır . Simülasyonun zaman adımı ve kamera örnekleme hızı,
aracın makul bir gecikme olmadan çevresini algılayabilmesi için yeterli düşük gecikme ile ayarlanmıştır
(örneğin 20 ms adım ile ~50 FPS).
ROS2 Altyapısı: Robot Operating System 2 (ROS2), robotik uygulamalar için yayınla/abonel ol tabanlı
(publish-subscribe) bir mimari sunar. Bu projede ROS2, Webots ile entegrasyon için kullanılmış ve
modüler bir yazılım mimarisi kurulmuştur. Webots içindeki araç modeli, ROS2'nin bir düğümü (node)
olarak çalıştırılan bir köprü denetleyicisi (örneğin webots_ros2 paketi) aracılığıyla ROS2 ağına bağlanır.
Bu sayede Webots'taki sensör verileri ROS2 mesajlarına dönüştürülerek yayınlanabilir ve ROS2 üzerinden
araca kontrol komutları gönderilebilir. Özellikle, araç kamerasından alınan görüntüler ROS2'nin
sensor_msgs/Image mesajları formatında bir /camera/image konusuna yayınlanmaktadır. Ayrıca, aracı
kontrol etmek için ROS2 üzerinde bir /cmd_vel (geometrik Twist mesajları ile hız ve direksiyon komutu)
veya uygun ise Ackermann sürüş mesajı kullanılmaktadır.
Python & OpenCV Tabanlı Görüntü İşleme: Görüntü işleme algoritması Python dilinde geliştirilmiştir.
ROS2 üzerinde bir görüntü işleme düğümü (node) olarak çalıştırılan bu yazılım, rclpy kullanılarak hem
görüntü verisini alır hem de kontrol komutu üretir. OpenCV kütüphanesi, kamera görüntülerinin
işlenmesinde kullanılmıştır. ROS2 ve OpenCV entegrasyonu için cv_bridge paketiyle ROS görüntü
mesajlarının OpenCV formatındaki (numpy dizisi) görüntülere dönüştürülmesi sağlanmıştır. Bu düğüm,
/camera/image konusuna abone olarak her yeni kareyi alır, tanımlanan şerit tespit algoritmasını uygular ve
hesapladığı direksiyon/sürüş komutunu (örneğin yön açısı ya da teker hızı) ilgili kontrol konusuna yayınlar.Görüntü İşleme Algoritması
Geliştirilen şerit tespit algoritması, geleneksel bilgisayarlı görü tekniklerini ardışık adımlar halinde
uygulayarak görüntüden şerit çizgilerini çıkarmaktadır. Temel adımlar ve kullanılan formüller aşağıda
detaylandırılmaktadır:
1.
2.
3.
4.
5.
Renk Uzayı Dönüşümü: Kameradan alınan ham görüntü genellikle RGB (Webots'da default
olarak RGB) formatındadır. Şerit çizgilerini arka plandan ayırt etmek için uygun bir renk uzayına
dönüşüm yapılır. Bu projede sarı veya beyaz renkli şerit çizgilerini daha kolay izole etmek
amacıyla HSV (Hue-Saturation-Value) renk uzayına dönüşüm kullanılmıştır. HSV uzayında renk
ve parlaklık daha ayrık şekilde temsil edildiğinden, belirli bir renk aralığını eşiklemek (threshold)
daha kolaydır. OpenCV ile bu dönüşüm cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
fonksiyonu ile gerçekleştirilir.
Renk Eşikleme (Maskeleme): Dönüştürülen HSV görüntüde, şerit çizgisinin rengine karşılık
gelen bir renk aralığı tanımlanarak maske oluşturulur. Örneğin, sarı şerit çizgileri için HSV
uzayında alt ve üst eşik değerleri tanımlanır (örneğin alt eşik [20, 100, 100], üst eşik [30, 255,
255] şeklinde). OpenCV ile cv2.inRange(hsv, lower, upper) fonksiyonu, bu aralık içinde kalan
pikselleri beyaz (255), diğerlerini siyah (0) yaparak ikili (binary) bir maske görüntüsü elde eder.
Bu maske, görüntüde yalnızca şerit çizgilerine ait piksellerin (renk açısından) seçilmesini sağlar ve
arka plandaki diğer nesneleri veya renkleri elimine eder. Sonuç olarak, örneğin yolun gri/asfalt
kısmı ve çevre nesneleri maskede siyah (0) değer alırken, sarı (veya beyaz) şerit çizgilerinin
bulunduğu bölgeler beyaz (255) olarak belirir.
Gürültü Giderme (Önişleme): Maske görüntüsü elde edildikten sonra, kenar tespitine geçmeden
önce görüntünün pürüzsüzleştirilmesi faydalı olabilir. Yüksek frekanslı gürültüler, kenar algılama
sırasında istenmeyen yanlış kenarlara yol açabileceğinden, maske üzerinde bir bulanıklaştırma
filtresi uygulanır. Genellikle Gauss bulanıklaştırma tercih edilir; bu işlemde komşu piksellere
Gaussian dağılımına göre ağırlık verilerek her piksel yeniden hesaplanır. Böylece küçük parazitler
yumuşatılarak, kenar dedektörünün daha tutarlı sonuç vermesi sağlanır. Bu adım her ne kadar
opsiyonel olsa da, simülasyonda kamera görüntüsü ideal koşullarda olduğundan gürültü seviyesi
düşük olabilir; buna rağmen Gauss filtresi kullanımı, kenar tespitinin kararlı olması için iyi bir
uygulamadır.
İlgi Bölgesi (ROI) Sınırlandırması: Kameranın görüş alanında, zemindeki şeritlerin bulunması
muhtemel bölge genellikle görüntünün alt kısmındadır (yolun ileriye doğru uzanan kısmı).
Gereksiz kenarları ve ilgisiz bölgeleri (örneğin gökyüzü, araç üst kısımları vb.) dikkate almamak
için bir ilgi bölgesi (Region of Interest) uygulaması yapılır. Bu projede ROI, görüntünün alt
yarısı olarak tanımlanmıştır. Bunun için, kenar görüntüsüne aynı boyutta siyah bir maske
oluşturulur ve yalnızca alt yarıyı kapsayan dörtgen (veya poligon) bölge beyaz (aktif) bırakılır.
Şerit Çizgilerinin Tanınması ve Ortalama: Tespit edilen çizgi parçalarının, sol ve sağ şerit
çizgilerini temsil eden iki ana doğruya indirgenmesi gerekmektedir. Genellikle yolun solundaki
şerit çizgisi ve sağındaki şerit çizgisi konum ve eğim (eğim açısı) bakımından ayırt edilebilir.
Örneğin, kameradan bakıldığında sol taraftaki şerit çizgisi yükseliyormuş (ekranın üstüne doğru
gidiyormuş) gibi görüneceği için negatif bir eğime (sola yatık) sahip olacaktır; sağ taraftaki şerit
ise pozitif eğimli olacaktır. Bu nedenle, bulunan her bir çizgi parçasının eğimi hesaplanarak (m =
(y2 - y1) / (x2 - x1) formülü ile) negatif eğimli olanlar sol şerit adayları, pozitif eğimli olanlar
sağ şerit adayları olarak ayrılır. Ayrıca görüntünün orta sütununa göre de sınıflandırma
yapılabilir: çizginin tüm noktaları görüntü genişliğinin orta noktasından sol tarafta ise sol şerit
grubuna, sağındakiler sağ şerit grubuna atılabilir. Ayrılan sol ve sağ çizgi parçaları için, bunların
birbirine yakın olanlarının ortalaması alınarak tek bir sol ve tek bir sağ çizgi elde edilir. Bu amaçla
eğim-intercept formunda ortalama yapmak yaygındır: her bir sol çizgi parçası için (m, b) değerleri
hesaplanır (y = m x + b formülüyle) ve bu değerlerin ortalaması alınarak görüntüde tek bir sol6.
7.
şerit doğrusu elde edilir. Sağ taraf için aynı işlem yapılır. Alternatif bir yaklaşım, tespit edilen
çizgi uç noktalarını (x1,y1,x2,y2) ortalamaktır. Örneğin sol çizgiler listesinde tüm x1’lerin,
y1’lerin, x2’lerin, y2’lerin ayrı ayrı ortalaması alınarak ortalama bir çizgi tanımlanabilir. Bu
işlemler sonucunda, kamera görüntüsünde iki ana doğru (sol ve sağ şerit çizgileri) matematiksel
olarak elde edilmiş olur.
Kontrol için Sapma Açısının Hesaplanması: Aracın şerit içinde kalması için, şeritlerin ortasına
göre bir yönlendirme yapılması gerekir. Hesaplanan sol ve sağ şerit doğrularını kullanarak aracın
şerit merkeziyle olan konum hatasını belirleyebiliriz. Bir yaklaşım, görüntünün alt orta noktasını
(aracın ilerlediği varsayılan çizgi) referans alıp, şerit çizgilerinin alt kesim noktalarına (araca en
yakın noktalarına) bakmaktır. Örneğin, sol ve sağ şerit çizgilerinin en alt (görüntü tabanına en
yakın) noktalarının x koordinatları alınabilir (left_x2 ve right_x2 gibi). Bu iki değer
ortalamasından, görüntü orta noktasının x koordinatı çıkarılarak aracın şerit merkezine göre ne
kadar kaydığı bulunur:
ROS2 ile Kontrol Komutu Yayını: Son adımda, hesaplanan sapma açısı veya direksiyon
komutu, ROS2 ağı üzerinden aracı kontrol eden ilgili düğüme iletilir. Webots üzerinde araç
modeli diferansiyel sürüşe sahip ise (örneğin TurtleBot tabanlı bir robot veya basit iki tekerlekli
bir robot), geometry_msgs/Twist mesajı ile açısal hız (yaw rotasyonu) komutu verilebilir. Eğer
otomobil tipi (Ackermann) bir model ise, direksiyon açısı ve hız için özel bir mesaj gönderilebilir.
Bu algoritmanın özet akış şeması, girdi video karelerinin okunması, renk uzayı dönüşümü ve maskeleme,
kenar bulma, ilgi bölgesi kırpma ile çizgi tespiti ve sonuçta çizgilerden konum hatası hesaplayarak
direksiyon komutu üretilmesi adımlarını içerir.
Simülasyon Verisi
Webots simülasyonunda araç üzerine monte edilen kamera, gerçek zamanlı olarak aracın görüş açısındaki
yol görüntüsünü sağlamıştır. Bu kamera, aracın önünde belirli bir açıyla ileriye bakacak şekilde
konumlandırılmıştır. Simülasyon verisi, gerçek bir kameradan alınan görüntülerin sanal karşılığıdır:
Webots ortamında tanımlanmış yol ve şerit geometrisine uygun olarak oluşturulan sentetik görüntüler
ardışıl olarak elde edilmiştir. Araç sabit bir hızla ilerlerken, her zaman adımında kameradan yeni bir
görüntü alınmış ve ROS2 üzerinden görüntü işleme algoritmasına iletilmiştir. Kamera görüntülerinde yolun
her iki yanında veya ortasında şerit çizgileri görünmektedir. Örneğin, tipik bir senaryoda asfalt gri renkte,
şerit çizgileri ise sarı renkte olup arka planla kontrast oluşturacak şekilde ayarlanmıştır.
Simülasyon ortamından elde edilen veriler, kontrollü ve etiketli olduğundan geleneksel algoritmanın test
edilmesi için uygun bir zemindir. Gerçek dünyanın aksine, Webots simülasyonunda ışıklandırma, kamera
paraziti veya şerit çizgilerinin silikliği gibi sorunlar minimize edilmiştir. Bu sayede algoritma, ideal
koşullarda kapasitesini gösterebilmiş ve temel zorluk unsurları (ör. değişken aydınlatma) olmadan
doğruluğu gözlemlenebilmiştir.
Deneysel Sonuçlar
Geliştirilen şerit takip sistemi, Webots üzerinde oluşturulan senaryolarda test edilmiştir. Gözlemsel
değerlendirme, sistemin işlevselliğini ve tepkilerini nitel olarak ölçmemizi sağladı. Test sırasında araç,başlangıçta şerit merkezinde kalacak şekilde konumlandırılmış ve sabit bir ileri hız verilerek yol boyunca
hareket etmesi sağlanmıştır.
Deneyler sonucunda, araç kamerasından gelen görüntülerin gerçek zamanlı olarak işlenebildiği ve aracın
şerit içinde kalacak biçimde direksiyon kontrolü yapılabildiği gözlemlenmiştir. Araç, düz yol kesimlerinde
şeritleri kararlılıkla takip edebilmiştir; şerit merkezine göre sapma oluştuğunda algoritma bunu hızlıca
tespit ederek uygun yöne dönüş komutu üretmiş ve araç yeniden merkeze yönelmiştir. Virajlı yollarda,
sistem belirli bir tepki gecikmesiyle de olsa (görüntü işleme ve komut döngüsünün frekansına bağlı olarak
milisaniye mertebelerinde bir gecikme) aracı şerit içinde tutmayı başarmıştır. Özellikle yumuşak virajlarda
aracın çizgiyi rahatlıkla takip ettiği, keskin virajlarda ise hafif gecikmeli düzeltmeler yaparak çizgi
yakınında kaldığı görüldü.
Performans metriği olarak sayısal bir değer kullanılmamış olsa da, gözlemsel başarı aracın sürekli olarak
yol şeritleri arasında kalması ve çizgilere tehlikeli derecede yaklaşmaması ile değerlendirildi. Test boyunca
araç hiçbir zaman şeridin dışına tamamen çıkmamış, dolayısıyla sistemin temel amacına ulaştığı
doğrulandı. Ayrıca, araç hareket halindeyken şerit algılama algoritmasının kararlı çalıştığı; görüntüde ani
değişimler olmadığı sürece (örneğin yol dışı büyük cisimler, beklenmedik ışık parlamaları vb.) yanlış
pozitif veya yanlış negatif algılamaların gözlenmediği not edilmiştir.
Bununla birlikte, sistemin bazı kısıtları deneysel gözlemle fark edilmiştir. Örneğin, yol üzerinde şerit
çizgisi kesildiğinde veya kaybolduğunda , geleneksel algoritma kısa bir an için kararsız kalabilmekte, ancak
son görülen çizgi doğrultusunda bir süre daha aracı yönlendirmeye devam etmektedir. Çok keskin
virajlarda veya dönemeçlerde, kameranın görüş açısından şerit çizgilerinin çıkması halinde algoritma yeni
bir çizgi algılayana kadar mevcut direksiyon açısını 0 derrece olarak korumaktadır ki bu da gerçek araç
kontrolünde riskli olabilir. Simülasyonda bu durum güvenlik sorunu yaratmasa da, algoritmanın sınırlarını
göstermesi açısından önemlidir.
Genel olarak, elde edilen sonuçlar, OpenCV tabanlı geleneksel görüntü işleme yaklaşımlarının temel bir
şerit takip görevi için yeterli olabileceğini ortaya koymuştur. Sistem gerçek zamanlı çalışmış ve ROS2 ile
Webots entegrasyonunun sorunsuz olduğu görülmüştür. Sonraki çalışmalarda, bu sistemin performansını
sayısal olarak ölçmek için örneğin “ortalama şeritten sapma mesafesi” veya “virajlı yolda şerit koruma
başarım yüzdesi” gibi metrikler tanımlanabilir.
Tartışma
Bu projede kullanılan yöntem, geleneksel görüntü işleme tekniklerine dayanmaktadır. Renk eşikleme,
kenar bulma ve Hough dönüşümü gibi adımlar, insan tarafından belirlenmiş kural ve eşik değerleri ile
çalışır. Bu yaklaşımın önemli avantajlarından biri, anlaşılır ve yorumlanabilir olmasıdır: algoritmanın her
adımı ne yaptığı bilinebilir, ara çıktı görüntüleri incelenerek hangi aşamada sorun olduğu saptanabilir.
Ayrıca, nispeten düşük hesaplama gücüyle çalışabilir; bu projede Python ile gerçek zamanlı olarak
çalışması, karmaşık bir derin sinir ağına kıyasla işlemci üzerinde hafif bir yük getirmiştir. Küçük bir eğitim
robotu ya da gömülü bir sistemde bile benzer algoritmalar, donanım hızlandırma olmadan çalıştırılabilir.
Uygulamada görüldüğü üzere, iyi koşullarda (net şerit çizgileri, sabit aydınlatma) klasik yöntemler şerit
tespitini başarıyla gerçekleştirebilmektedir.
Öte yandan, geleneksel yaklaşım ortam koşullarına duyarlıdır. Renk eşik değerleri veya Canny kenar
eşikleri, ortam ışığı değiştiğinde, gölgeler belirdiğinde veya şerit boya rengi farklılaştığında güncellenmek
zorunda kalabilir. Klasik algoritmalar genelde belirli varsayımlarla çalışır: örneğin şerit çizgisinin belirli bir
renk aralığında olması, kenarların yeterince belirgin olması gibi. Bu varsayımlar bozulduğunda (örneğingece sürüşünde zayıf görünen şeritler, aşınmış yol çizgileri veya yol üzerinde birikmiş su/kar ile silinmiş
çizgiler) performans keskin biçimde düşebilir. Derin öğrenme tabanlı yöntemler ise daha yüksek esneklik
ve dayanıklılık vadediyor. Örneğin, bir derin öğrenme modeli farklı aydınlatma koşullarında veya farklı
tür şerit biçimlerinde (düz, kesik, çift çizgi vs.) eğitilirse, yeni bir kural yazmaya gerek kalmadan bunları
algılayabilir. Erken dönem şerit tespit yöntemleri tamamen kenar tespiti, renk eşikleme gibi tekniklere
dayanırken, günümüzde derin öğrenme ile çok daha yüksek doğruluklar elde edilmiştir. Derin öğrenme
modelleri, görüntüden özelliği kendisi öğrenerek, insan gözünün fark etmekte zorlanacağı ipuçlarını da
kullanabilir.
Derin öğrenme yaklaşımlarının önemli bir avantajı, genelleme yeteneğidir. Örneğin, bir evrişimsel sinir ağı
tabanlı şerit tespit algoritması, eğitim verisinde gördüğü farklı senaryolar sayesinde gerçek dünyada
karşılaşacağı beklenmedik durumlara daha hazırlıklı olabilir. Yağmur, sis, düşük ışık, yol çalışması
nedeniyle değişen çizgiler gibi durumlarda derin öğrenme tabanlı bir model geleneksel eşik-tabanlı bir
filtreden daha başarılı sonuç verebilir. Literatürde, görüntü segmentasyonu yaklaşımıyla piksel bazında
şerit çizgisi tespiti yapan modellerden, özellik haritaları öğrenerek çıktıyı doğru parametrelerine çeviren
(örneğin polinom olarak şerit eğrisini çıktılarken) modellere kadar çeşitli derin öğrenme yöntemleri
geliştirilmiştir. Bu modeller, çok sayıda örnekle eğitildikleri için perspektif bozulması, araç kamerasının
farklı açılarda olması gibi konularda insan tarafından kural yazmadan çözüm sunabilmektedir.
Ancak derin öğrenme yaklaşımlarının da dezavantajları yok değildir. Veri ihtiyacı bunların başında gelir –
iyi bir model için çeşitli koşulları kapsayan binlerce etiketlenmiş görüntü gerekebilir. Ayrıca, derin ağların
gerçek zamanlı çalışması ciddi hesaplama gücü ister; GPU olmadan, özellikle yüksek çözünürlükteki
kameralar için istenen fps değerlerine ulaşmak zor olabilir. Gömülü sistemlerde derin öğrenme kullanmak,
genellikle ekstra donanım (GPU, TPU veya hızlandırıcılar) gerektirmektedir. Buna karşın, geleneksel
yöntemler çok daha hafif ve hızlıdır, fakat her yeni durum için elle ayar yapılması gerekir. Örneğin, aynı
algoritmayı farklı renk yol çizgileri için kullanmak istersek, renk eşiklerini yeniden tanımlamamız gerekir;
derin öğrenmede ise modelin yeniden eğitilmesi gerekebilir, ki bu da zaman alıcıdır ancak bir kez
eğitildikten sonra model anlık olarak rengi kendi ayırt edebilir.
Sonuç olarak, bu projede uygulanan geleneksel OpenCV tabanlı şerit takip sistemi, belirli koşullar altında
tatmin edici bir performans sergilemiştir ve anlaşılır yapısıyla geliştirme kolaylığı sağlamıştır. Gelecekte,
bu sisteme derin öğrenme entegrasyonu yapılarak daha zorlu senaryolara uyum sağlama kabiliyeti
artırılabilir. Örneğin, klasik algoritma ile tespit edilen şerit adayları, bir sinir ağı ile doğrulanarak yanlış
pozitifler elenebilir ya da doğrudan kamera görüntüsünden öğrenme ile çalışan bir model gerçek zamanlı
olarak direksiyon açısını tahmin edebilir. Akademik çalışmalar, geleneksel görüntü işlemeden derin
öğrenmeye geçişin şerit tespitinde doğruluk ve güvenilirlik açısından büyük ilerlemeler kaydettiğini
göstermektedir. Yine de, mühendislikte çoğu zaman hibrit yaklaşımlar faydalı olur: pratik bir otonom sürüş
sisteminde, derin öğrenmenin güçlü olduğu durumlarla klasik yöntemlerin verimli olduğu durumlar bir
arada kullanılarak hem hesaplama yükü optimize edilebilir hem de güvenlik artırılabilir. Bu projenin
çıktıları, böylesi bir ileri çalışma için temel teşkil etmekte ve farklı yöntemlerin karşılaştırmalı
değerlendirilmesine olanak sunmaktadır.
Kaynaklar
[1] OpenCV Library: https://opencv.org
[2] Raspberry Pi Foundation, “Raspberry Pi 4 Model B,” https://www.raspberrypi.com
[3] A. Yazar, “Görüntü İşleme ile Şerit Takibi,” IEEE Türkiye Öğrenci Kolu, 2023.
