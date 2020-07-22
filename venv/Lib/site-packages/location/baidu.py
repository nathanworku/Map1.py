import math

class Baidu (object) :
    city_mapping = {
        '北京市' : {
            'cid' : 131
        },
        '上海市' : {
            'cid' : 289
        },
        '广州市' : {
            'cid' : 257
        },
        '深圳市' : {
            'cid' : 340
        },
        '南京市' : {
            'cid' : 315
        },
        '天津市' : {
            'cid' : 332
        },
        '成都市市' : {
            'cid' : 75
        },
    }

    def getShiftPoint(self, geo, s_lng = 0, s_lat = 0) :
        # lng 、lat 经纬度
        lat = float(geo['lat'])
        lng = float(geo['lng'])
        half = 6371
        s_lng = float(s_lng) / 1000
        s_lat = float(s_lat) / 1000

        dlng = 2 * math.asin(math.sin(s_lng/ (2 * half)) / math.cos(math.radians(lat)))
        dlng = math.degrees(dlng)
        dlat = s_lat/ half
        dlat = math.degrees(dlat)
        fourpoint = (
            {'lat' : round(lat + dlat, 8), 'lng' : round(lng + dlng,8)}
        )
        return fourpoint

    # 根据两点间的经纬度计算距离
    def getDistance(self, geo1, geo2) :
        lat1 = float(geo1['lat'])
        lng1 = float(geo1['lng'])
        lat2 = float(geo2['lat'])
        lng2 = float(geo2['lng'])

        #approximate radius of earth in meters
        earthRadius = 6367000

        lat1 = (lat1 * math.pi) / 180
        lng1 = (lng1 * math.pi) / 180

        lat2 = (lat2 * math.pi) / 180
        lng2 = (lng2 * math.pi) / 180

        calcLongitude = lng2 - lng1
        calcLatitude = lat2 - lat1
        stepOne = pow(math.sin(calcLatitude / 2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(calcLongitude / 2), 2)
        stepTwo = 2 * math.asin(min(1, math.sqrt(stepOne)))
        calculatedDistance = earthRadius * stepTwo

        return round(calculatedDistance)

    def  mercatorToLngLat (self, mLngLat) :
        absLngLat = {
            'lng' : abs(float(mLngLat['lng'])),
            'lat' : abs(float(mLngLat['lat']))
        }
        for i in range(len(self.__MCBAND)) :
            if absLngLat['lat'] >= self.__MCBAND[i] :
                mc = self.__MC2LL[i]
                break

        lngLat = self.__convertor(mLngLat, mc)
        lngLat = {
            'lng' :  round(lngLat['lng'], 8),
            'lat' :  round(lngLat['lat'], 8)
        }
        return lngLat

    def lngLatToMercator (self, point) :
        point['lng'] = self.__getLoop(float(point['lng']), -180, 180)
        point['lat'] = self.__getRange(float(point['lat']), -74, 74)
        lng_lat = {
            'lng' : point['lng'],
            'lat' : point['lat']
        }
        for i in range(len(self.__LLBAND)) :
            if (lng_lat['lat'] >= self.__LLBAND[i]) :
                mc = self.__LL2MC[i]
                break
        if (not mc) :
            for i in range(len(self.__LLBAND)-1 , -1, -1) :
                if (lng_lat['lat'] <= -self.__LLBAND[i]) :
                    mc = self.__LL2MC[i]
                    break
        cE = self.__convertor(point, mc)
        lng_lat = {
            'lng' : round(cE['lng'], 2),
            'lat' : round(cE['lat'], 2)
        }
        return lng_lat

    def __getLoop (self, lng, a, b) :
        while (lng >b) :
            lng -= (b - a)

        while (lng <a) :
            lng += (b - a)
        return lng

    def __getRange (self, lat,a,b) :
        if a != None :
            lat = max(lat,a)
        if b != None :
            lat = min(lat,b)
        return lat

    def  __convertor (self, point, mc) :
        if not point or not mc :
            return

        lng = mc[0] + mc[1] * abs(point['lng'])
        c = abs(point['lat']) /mc[9]
        lat = mc[2] +mc[3] *c +mc[4] *c *c +mc[5] *c *c *c +mc[6] *c *c *c *c +mc[7] *c *c *c *c *c +mc[8] *c *c *c *c *c *c
        lng *= -1 if point['lng'] < 0 else 1
        lat *= -1 if point['lat'] < 0 else 1
        return {'lng':lng,'lat' :lat}


    def pixelTopoint(self, point, zoom, center, bounds) :
        # 像素到坐标
        if not point :
            return
        zoomUnits = self.__getzoomUnits(zoom)
        mercatorlng = center['lng'] + zoomUnits * (point['x'] - bounds['width'] / 2)
        mercatorLat = center['lat'] - zoomUnits * (point['y'] - bounds['height'] / 2)
        mercatorlngLat = {'lng' :  mercatorlng, 'lat' :  mercatorLat}
        return self.mercatorToLngLat(mercatorlngLat)

    def pointToPixel (self, point, zoom, mcenter, bounds) :
        # 坐标到像素
        if not point :
            return

        point = self.lngLatToMercator(point)
        units = self.__getzoomUnits(zoom)
        x = round((point['lng'] - mcenter['lng']) / units + bounds['width'] / 2)
        y = round((mcenter['lat'] - point['lat']) / units + bounds['height'] / 2)
        return {
            'x' : x,
            'y' : y
        }

    def __getzoomUnits(self, zoom) :
        return pow(2, (18 - zoom))

    __MCBAND = (12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0)
    __LLBAND = (75, 60, 45, 30, 15, 0)
    __MC2LL = (
        (1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547, 91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2),
        ( - 7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826, -59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86), 
        ( - 3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871, -25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37),
        ( - 1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277, -4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06),
        (3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511, -0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4),
        (2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994, -0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5)
    )
    __LL2MC = (
        ( - 0.0015702102444, 111320.7020616939, 1704480524535203, -10338987376042340, 26112667856603880, -35149669176653700, 26595700718403920, -10725012454188240, 1800819912950474, 82.5),
        (0.0008277824516172526, 111320.7020463578, 647795574.6671607, -4082003173.641316, 10774905663.51142, -15171875531.51559, 12053065338.62167, -5124939663.577472, 913311935.9512032, 67.5),
        (0.00337398766765, 111320.7020202162, 4481351.045890365, -23393751.19931662, 79682215.47186455, -115964993.2797253, 97236711.15602145, -43661946.33752821, 8477230.501135234, 52.5),
        (0.00220636496208, 111320.7020209128, 51751.86112841131, 3796837.749470245, 992013.7397791013, -1221952.21711287, 1340652.697009075, -620943.6990984312, 144416.9293806241, 37.5),
        ( - 0.0003441963504368392, 111320.7020576856, 278.2353980772752, 2485758.690035394, 6070.750963243378, 54821.18345352118, 9540.606633304236, -2710.55326746645, 1405.483844121726, 22.5),
        ( - 0.0003218135878613132, 111320.7020701615, 0.00369383431289, 823725.6402795718, 0.46104986909093, 2351.343141331292, 1.58060784298199, 8.77738589078284, 0.37238884252424, 7.45)
    )
