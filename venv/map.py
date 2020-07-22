import folium

#create map object
m= folium.Map(location= [43.651070,-79.347015], zoom_start=12)

#Global tooltip

tooltip1= "Homicide #1"
tooltip2= "Homicide #2"
tooltip3= "Homicide #3"
tooltip4= "Homicide #4"
tooltip5= "Homicide #5"
tooltip6= "Homicide #6"
tooltip7= "Homicide #7"
tooltip8= "Homicide #8"
tooltip9= "Homicide #9"
tooltip10= "Homicide #10"
tooltip11= "Homicide #11"
tooltip12= "Homicide #12"
tooltip13= "Homicide #13"
tooltip14= "Homicide #14"
tooltip15= "Homicide #15"
tooltip16= "Homicide #16"
tooltip17= "Homicide #17"
tooltip18= "Homicide #18"
tooltip19= "Homicide #19"
tooltip20= "Homicide #20"
tooltip21= "Homicide #21"
tooltip22= "Homicide #22"
tooltip23= "Homicide #23"
tooltip24= "Homicide #24"
tooltip25= "Homicide #25"
tooltip26= "Homicide #26"
tooltip27= "Homicide #27"
tooltip28= "Homicide #28"
tooltip29= "Homicide #29"
tooltip30= "Homicide #30"
tooltip31= "Homicide #31"
tooltip32= "Homicide #32"
tooltip33= "Homicide #33"
tooltip34= "Homicide #34"
tooltip35= "Homicide #35"
tooltip36= "Homicide #36"
tooltip37= "Homicide #37"

#Create custom marker icon
LogoIcon= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon2= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon3= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon4= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon5= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon6= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon7= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon8= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon9= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon10= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon11=folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon12= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon13= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon14= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon15= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon16= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon17= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon18= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon19= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon20= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon21= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon22= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon23= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon24= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon25= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon26= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon27= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon28= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon29= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon30= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon31= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon32= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon33= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon34= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon35= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon36= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))
LogoIcon37= folium.features.CustomIcon("Logo2.png", icon_size=(50,50))


#create markers
folium.Marker([43.6482182, -79.3789029],
              popup="<strong>Bob Marley, 52</strong>",
              tooltip= tooltip1,
                icon =LogoIcon).add_to(m),
folium.Marker([43.56878453611069, -79.56878463611069],
              popup="<strong>Bob Marley, 52</strong>",
              tooltip= tooltip2,
                icon=LogoIcon2).add_to(m),
folium.Marker([43.5482182, -79.5789029],
              popup="<strong>Deez Nuts2, 52</strong>",
              tooltip= tooltip3,
                icon =LogoIcon3).add_to(m)
folium.Marker([43.43222182, -79.332489029],
              popup="<strong>Deez Nuts3, 52</strong>",
              tooltip= tooltip4,
                icon =LogoIcon4).add_to(m)
folium.Marker([43.6844463, -79.4325256],
              popup="<strong>Jan 20, Giulia Matthews, 54</strong>",
              tooltip= tooltip5,
                icon =LogoIcon5).add_to(m)
folium.Marker([43.32482182, -79.4320029],
              popup="<strong>Deez Nuts5, 52</strong>",
              tooltip= tooltip6,
                icon =LogoIcon6).add_to(m)
folium.Marker([43.6390568, -79.3985367],
              popup="<strong>Jan 31, Jalen Colley, 21</strong>",
              tooltip= tooltip7,
                icon =LogoIcon7).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts7, 52</strong>",
              tooltip8= tooltip8,
                icon =LogoIcon8).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip9= tooltip9,
                icon =LogoIcon9).add_to(m)
folium.Marker([43.6529691, -79.5726013],
              popup="<strong>Deandre Campbell-Kelly, 29, died from his gun shot wounds </strong>",
              tooltip= tooltip10,
                icon =LogoIcon10).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip11= tooltip11,
                icon =LogoIcon11).add_to(m)
folium.Marker([43.7319102, -79.4589615],
              popup="<strong>Feb 25, Ashley Noel Arzaga, 24 </strong>",
              tooltip= tooltip12,
                icon =LogoIcon12).add_to(m)
folium.Marker([43.7094548, -79.5089149],
              popup="<strong>Deez March 2, Man pronounced dead from gun shot wounds</strong>",
              tooltip= tooltip13,
                icon =LogoIcon13).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip14= tooltip14,
                icon =LogoIcon14).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip15= tooltip15,
                icon =LogoIcon15).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip16= tooltip16,
                icon =LogoIcon16).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip17= tooltip17,
                icon =LogoIcon17).add_to(m)
folium.Marker([43.742432182, -79.372349029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip18= tooltip18,
                icon =LogoIcon18).add_to(m)
folium.Marker([43.744322182, -79.34329029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip19= tooltip19,
                icon =LogoIcon19).add_to(m)
folium.Marker([43.75232182, -79.38834029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip20= tooltip20,
                icon =LogoIcon20).add_to(m)
folium.Marker([43.6746386, -79.4583607],
              popup="<strong>April 8, Lindsay John Templeton, 37</strong>",
              tooltip= tooltip21,
                icon =LogoIcon21).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip22= tooltip22,
                icon =LogoIcon22).add_to(m)
folium.Marker([43.6169395, -79.4994736],
              popup="<strong>Djuro Orlovic of Toronto, 72,  was found with obvious signs of trauma and was later pronounced dead at the scene</strong>",
              tooltip= tooltip23,
                icon =LogoIcon23).add_to(m)
folium.Marker([43.7407163, -79.5061684],
              popup="<strong>Jeremiah Ranger, 15</strong>",
              tooltip= tooltip24,
                icon =LogoIcon24).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip25= tooltip25,
                icon =LogoIcon25).add_to(m)
folium.Marker([43.6974173, -79.3964767],
              popup="<strong>May 14, Peter Elie, 52</strong>",
              tooltip= tooltip26,
                icon =LogoIcon26).add_to(m)
folium.Marker([43.7472891, -79.5798111],
              popup="<strong>Hashim Kinani, 23</strong>",
              tooltip27= tooltip27,
                icon =LogoIcon27).add_to(m)
folium.Marker([43.7382182, -79.3639029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip28= tooltip28,
                icon =LogoIcon28).add_to(m)
folium.Marker([43.7483182, -79.3709029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip29= tooltip29,
                icon =LogoIcon29).add_to(m)
folium.Marker([43.7682182, -79.3829029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip30= tooltip30,
                icon =LogoIcon30).add_to(m)
folium.Marker([43.7402182, -79.3709029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip31= tooltip31,
                icon =LogoIcon31).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip32= tooltip32,
                icon =LogoIcon32).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip33= tooltip33,
                icon =LogoIcon33).add_to(m)
folium.Marker([43.74342182, -79.3889029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip34= tooltip34,
                icon =LogoIcon34).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip35= tooltip35,
                icon =LogoIcon35).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip36= tooltip36,
                icon =LogoIcon36).add_to(m)
folium.Marker([43.7482182, -79.3789029],
              popup="<strong>Deez Nuts, 52</strong>",
              tooltip37= tooltip37,
                icon =LogoIcon37).add_to(m)

# Circle marker
folium.CircleMarker(
    location=[43.6442182, -79.3779029],
    radius=60,
    popup="Homicide 1",
    fill=True,
    fill_color='#428bca'
).add_to(m)

# generate map
m.save("map.html")
