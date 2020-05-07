<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.12.0-București" styleCategories="AllStyleCategories" maxScale="1000" hasScaleBasedVisibilityFlag="0" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <rasterrenderer classificationMin="1.51556" classificationMax="40.92" band="1" type="singlebandpseudocolor" opacity="1" alphaBand="-1" nodataColor="">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>CumulativeCut</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader colorRampType="INTERPOLATED" clip="0" classificationMode="1">
          <colorramp name="[source]" type="gradient">
            <prop k="color1" v="255,245,240,255"/>
            <prop k="color2" v="103,0,13,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.13;254,224,210,255:0.26;252,187,161,255:0.39;252,146,114,255:0.52;251,106,74,255:0.65;239,59,44,255:0.78;203,24,29,255:0.9;165,15,21,255"/>
          </colorramp>
          <item color="#fff5f0" value="1.51555634307861" label="1.51555634307861" alpha="255"/>
          <item color="#fee0d2" value="6.63813678268433" label="6.63813678268433" alpha="255"/>
          <item color="#fcbba1" value="11.76071722229" label="11.76071722229" alpha="255"/>
          <item color="#fc9272" value="16.8832976618958" label="16.8832976618958" alpha="255"/>
          <item color="#fb6a4a" value="22.0058781015015" label="22.0058781015015" alpha="255"/>
          <item color="#ef3b2c" value="27.1284585411072" label="27.1284585411072" alpha="255"/>
          <item color="#cb181d" value="32.2510389807129" label="32.2510389807129" alpha="255"/>
          <item color="#a50f15" value="36.9795747711182" label="36.9795747711182" alpha="255"/>
          <item color="#67000d" value="40.9200212631226" label="40.9200212631226" alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="-6" brightness="34"/>
    <huesaturation grayscaleMode="0" colorizeBlue="11" colorizeStrength="39" saturation="0" colorizeRed="229" colorizeGreen="244" colorizeOn="0"/>
    <rasterresampler maxOversampling="2"/>
  </pipe>
  <blendMode>6</blendMode>
</qgis>
