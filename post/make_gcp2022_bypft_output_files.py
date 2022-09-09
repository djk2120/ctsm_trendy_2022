import Nio
import numpy as np
import glob
#import separate_clmhist_bypft

trendy='TRENDY2022'
sim='S2'
d='/glade/campaign/asp/djk2120/'+trendy+'/'+sim+'/lnd/proc/tseries/month_1/'
lai=glob.glob(d+'*h1.TLAI*')[0]
f1,f2=lai.split('TLAI')
datadir_out = '/glade/campaign/asp/djk2120/'+trendy+'/'+sim+'/lnd/proc/trendy/'


def clobber(filename):
    try:
        print('replacing file: '+filename)
        os.remove(filename)
    except:
        print('file does not exist: '+filename)


def separate_clmhist_bypft(file_in, variable_name=None, IM=None, JM=None, npft=None, verbose = True, pftcoords_file=None):
    """function to separate 1-D or 2_D vector of data into 3-D or 4-D array.  IM is the number of longitude gridpoints, JM is the number of latitude gridpoints, and npft is the number of PFTs.  input argument is the Nio object corresponding to the file you want to open."""
    #
    if type(file_in).__name__ != 'NioFile':
        raise RuntimeError
    #
    if pftcoords_file == None:
        pftcoords_file = file_in
        #
    pftvars = []
    for variable in file_in.variables:
        dims = file_in.variables[variable].dimensions
        if 'pft' in dims:
            pftvars.append(variable)
            #
    if not variable_name in pftvars:
        if variable_name == None:
            return pftvars
        else:
            print('variable '+variable_name+ ' not in pft variable list.')
            print(pftvars)
            raise RuntimeError
        #
    if IM==None:
        IM = np.max(pftcoords_file.variables['pfts1d_ixy'])
    if JM==None:
        JM = np.max(pftcoords_file.variables['pfts1d_jxy'])
    if npft==None:
        npft = np.max(pftcoords_file.variables['pfts1d_itype_veg'])+1 ## zero is valid pft
        #
    vardims = list(file_in.variables[variable_name].dimensions)
    print(vardims)
    ndims_in_wo_pft = len(vardims)-1
    ndims_out = ndims_in_wo_pft+3
    vardims.append('lat')
    vardims.append('lon')
    dims_out_size = []
    for i, dim in enumerate(vardims):
        if dim == 'lat':
            dims_out_size.append(JM)
        elif dim == 'lon':
            dims_out_size.append(IM)
        elif dim == 'pft':
            dims_out_size.append(npft)
            pftdim = i
        else:
            dims_out_size.append(file_in.dimensions[dim])
            #
    badno = file_in.variables[variable_name].attributes['missing_value'][0]
    #
    if ndims_in_wo_pft == 1:
        data_out = np.ma.masked_all(dims_out_size)
        for pft in range(npft):
            print(' running pft '+str(pft) + ' of '+str(npft))
            var_in = file_in.variables[variable_name]
            ### now loop over timesteps
            pftlonindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), pftcoords_file.variables['pfts1d_ixy'][:]) -1
            pftlatindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), pftcoords_file.variables['pfts1d_jxy'][:]) -1
            for i in range(dims_out_size[0]):
                # if i%10 == 0:
                #     print(' running pft '+str(i) + ' of '+str(dims_out_size[0]))
                varpft = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[0,:] < badno), var_in[i,:])
                varpftindices = pftlonindices + pftlatindices*IM + pft*IM*JM + i*npft*IM*JM
                data_out.flat[varpftindices] = varpft
                #
    elif ndims_in_wo_pft == 0:
        data_out = np.ma.masked_all(dims_out_size)
        for pft in range(npft):
            var_in = file_in.variables[variable_name]
            ### now loop over timesteps
            varpft = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), var_in[:])
            pftlonindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), pftcoords_file.variables['pfts1d_ixy'][:]) -1
            pftlatindices = np.extract(np.logical_and(pftcoords_file.variables['pfts1d_itype_veg'][:] == pft, var_in[:] < badno), pftcoords_file.variables['pfts1d_jxy'][:]) -1
            varpftindices = pftlonindices + pftlatindices*IM + pft*IM*JM 
            data_out.flat[varpftindices]= varpft
            #
    else:
        raise NotImplementedError
    #
    return data_out


    

pftname =   ["not_vegetated", 
             "needleleaf_evergreen_temperate_tree", 
             "needleleaf_evergreen_boreal_tree", 
             "needleleaf_deciduous_boreal_tree", 
             "broadleaf_evergreen_tropical_tree", 
             "broadleaf_evergreen_temperate_tree", 
             "broadleaf_deciduous_tropical_tree", 
             "broadleaf_deciduous_temperate_tree", 
             "broadleaf_deciduous_boreal_tree", 
             "broadleaf_evergreen_shrub", 
             "broadleaf_deciduous_temperate_shrub", 
             "broadleaf_deciduous_boreal_shrub", 
             "c3_arctic_grass", 
             "c3_non-arctic_grass", 
             "c4_grass", 
             "unmanaged_c3_crop", 
             "unmanaged_c3_irrigated", 
             "corn", 
             "irrigated_corn", 
             "spring_wheat", 
             "irrigated_spring_wheat", 
             "winter_wheat", 
             "irrigated_winter_wheat", 
             "soybean", 
             "irrigated_soybean",
             "barley",
             "irrigated_barley",
             "winter_barley",
             "irrigated_winter_barley",
             "rye",
             "irrigated_rye",
             "cassava",
             "irrigated_cassava",
             "citrus",
             "irrigated_citrus",
             "cocoa",
             "irrigated_cocoa",
             "coffee",
             "irrigated_coffee",
             "cotton",
             "irrigated_cotton",
             "datepalm",
             "irrigated_datepalm",
             "foddergrass",
             "irrigated_foddergrass",
             "grapes",
             "irrigated_grapes",
             "groundnuts",
             "irrigated_groundnuts",
             "millet",
             "irrigated_millet",
             "oilpalm",
             "irrigated_oilpalm",
             "potatoes",
             "irrigated_potatoes",
             "pulses",
             "irrigated_pulses",
             "rapeseed",
             "irrigated_rapeseed",
             "rice",
             "irrigated_rice",
             "sorghum",
             "irrigated_sorghum",
             "sugarbeet",
             "irrigated_sugarbeet",
             "sugarcane",
             "irrigated_sugarcane",
             "sunflower",
             "irrigated_sunflower",
             "miscanthus",
             "irrigated_miscanthus",
             "switchgrass",
             "irrigated_switchgrass",
             "tropical_corn",
             "irrigated_tropical_corn",
             "tropical_soybean",
             "irrigated_tropical_soybean"]


npft = 77





read_input_file = True
if read_input_file:
    vars_in = ['TLAI']

    pftcoords_file = Nio.open_file(lai)


    filein_list_exp2 = []

    for var_i, varname in enumerate(vars_in):
        print('starting var '+varname)
        #

        filename=f1+varname+f2
        filein_list_exp2.append(Nio.open_file(filename))

        #
        if var_i == 0:
            lats = filein_list_exp2[len(filein_list_exp2)-1].variables['lat']
            lons = filein_list_exp2[len(filein_list_exp2)-1].variables['lon']
            time = filein_list_exp2[len(filein_list_exp2)-1].variables['time']
            ntime_monthly = len(time[:])
            ntime_annual = ntime_monthly / 12
            JM = len(lats[:])
            IM = len(lons[:])
        locals()[varname+'_exp2'] = separate_clmhist_bypft(filein_list_exp2[len(filein_list_exp2)-1], variable_name=varname, IM=IM, JM=JM, npft=npft, pftcoords_file=pftcoords_file)
        #

    print('test 0')

    vars_out = ['mrso', 'mrro', 'evapotrans', 'sh', 'Ts', 'cVeg', 'cLitter', 'cSoil', 'gpp', 'ra', 'npp', 'rh', 'fFire', 'fLuc', 'nbp', 'landCoverFrac', 'lai', 'tsl', 'msl', 'evspsblveg', 'evspsblsoi', 'tran', 'swup', 'lwup', 'ghflx', 'snow_depth', 'swe', 'fGrazing', 'fHarvest', 'fVegLitter', 'fLitterSoil', 'fVegSoil', 'cLeaf', 'cWood', 'cRoot', 'cCwd', 'burntArea', 'cProduct', 'dlai', 'evapotranspft', 'transpft', 'evapo', 'cVegpft', 'gpppft', 'npppft','nbppft','tskinpft','irripft']

    exp_list = ['_exp2']
    exp_outputname_list = ['CLM5.0_'+sim+'_']

    units_out_list = ['kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'W m-2', 'K', 'kg m-2', 'kg m-2', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'None', 'None', 'K', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'W m-2', 'W m-2', 'W m-2', 'm', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2', 'kg m-2', 'kg m-2', 'kg m-2', '%', 'kg m-2', 'None', 'W m-2','W m-2','W m-2','kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'K', 'kg m-2 s-1']



    long_name_out_list = ['Total Soil Moisture Content', 'Total Runoff', 'Total Evapo-Transpiration', 'Sensible heat flux', 'Surface temperature', 'Carbon in Vegetation', 'Carbon in Above-ground Litter Pool', 'Carbon in Soil (including below-ground litter)', 'Gross Primary Production', 'Autotrophic (Plant) Respiration', 'Net Primary Production', 'Heterotrophic Respiration', 'CO2 Emission from Fire', 'CO2 Flux to Atmosphere from Land Use Change', 'Net Biospheric Production', 'Fractional Land Cover of PFT', 'Leaf Area Index', 'Temperature of Soil', 'Moisture of Soil', 'Evaporation from Canopy', 'Water Evaporation from Soil', 'Transpiration', 'Shortwave up radiation', 'Longwave up radiation', 'Ground heat flux', 'Snow Depth ', 'Snow Water Equivalent ', 'CO2 Flux to Atmosphere from Grazing', 'CO2 Flux to Atmosphere from Crop Harvesting', 'Total Carbon Flux from Vegetation to Litter', 'Total Carbon Flux from Litter to Soil', 'Total Carbon Flux from Vegetation Directly to Soil', 'Carbon in Leaves', 'Carbon in Wood', 'Carbon in Roots', 'Carbon in Coarse Woody Debris', 'Burnt Area Fraction', 'Carbon in Products of Land Use Change', 'Leaf Area Index Daily', 'Vegtype level evapotranspiration', 'Vegtype level transpiration','Vegtype level Soil evaporation','Vegtype level Carbon in Vegetation','Vegtype level GPP','Vegtype level NPP','Vegtype level NBP','Vegtype level Skin temperature','Vegtype level irrigation']


#############   lai   #############
varname_out = 'lai'
varname_in = 'TLAI'
unit_conversion = 1.
print(' test 1 '+varname_out)
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    print(' test 2 '+varname_out)
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        print(' test 3 '+varname_out)
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        print(' test 4')
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))

        file_varout[:] = data_out[:,pft_i, :, :].astype('float32')

        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out
    print(' end testing '+varname_out)

#NOTE: evapotrans isn't relevant at PFT-level due to shared soil column
#############   evapotranspft   #############
#varname_out = 'evapotranspft'
#varname_in = ['FCEV', 'FCTR', 'FGEV']
#unit_conversion = 1.
#try:
#    list_index = vars_out.index(varname_out)
#except:
#    list_index = -1
#for exp_i in range(len(exp_list)):    
#    for summation_i in range(len(varname_in)):
#        if summation_i == 0:
#            full_varname_string = varname_in[summation_i]
#            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
#        else:
#            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
#            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
#    np.ma.set_fill_value(data_out, -99999.)
#    for pft_i in range(npft):
#        #
#        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
#        clobber(filename_out)
#        file_out = Nio.open_file(filename_out, 'c')
#        file_out.create_dimension('lat', JM)
#        file_out.create_dimension('lon', IM)
#        file_out.create_dimension('time', ntime_monthly)
#        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
#        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
#        file_timevarout = file_out.create_variable('time', 'f', ('time',))
#        file_latvarout[:] = lats[:]
#        file_lonvarout[:] = lons[:]
#        file_timevarout[:] = time[:]
#        for i, att in enumerate(lats.attributes):
#            setattr(file_out.variables['lat'],att,lats.attributes[att])
#        for i, att in enumerate(lons.attributes):
#            setattr(file_out.variables['lon'],att,lons.attributes[att])
#        for i, att in enumerate(time.attributes):
#            setattr(file_out.variables['time'],att,time.attributes[att])
#        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
#        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
#        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
##         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
#        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
##         for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
##             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
#        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
#        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',full_varname_string)
#        file_out.close()
#    del data_out

    
 #############   transpft   #############
varname_out = 'transpft'
varname_in = 'FCTR'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
       #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out

    
# #############   evapo   #############
#varname_out = 'evapo'
#varname_in = 'FGEV'
#unit_conversion = 1.
#try:
#    list_index = vars_out.index(varname_out)
#except:
#    list_index = -1
#for exp_i in range(len(exp_list)):    
#    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
#    np.ma.set_fill_value(data_out, -99999.)
#    for pft_i in range(npft):
#        #
#        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
#        clobber(filename_out)
#        file_out = Nio.open_file(filename_out, 'c')
#        file_out.create_dimension('lat', JM)
#        file_out.create_dimension('lon', IM)
#        file_out.create_dimension('time', ntime_monthly)
#        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
#        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
#        file_timevarout = file_out.create_variable('time', 'f', ('time',))
#        file_latvarout[:] = lats[:]
#        file_lonvarout[:] = lons[:]
#        file_timevarout[:] = time[:]
#        for i, att in enumerate(lats.attributes):
#            setattr(file_out.variables['lat'],att,lats.attributes[att])
#        for i, att in enumerate(lons.attributes):
#            setattr(file_out.variables['lon'],att,lons.attributes[att])
#        for i, att in enumerate(time.attributes):
#            setattr(file_out.variables['time'],att,time.attributes[att])
#        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
#        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
#        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
##         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
#        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
##         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
##             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
#        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
#        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
#        file_out.close()
#    del data_out

#############   cVegpft   #############
varname_out = 'cVegpft'
varname_in = 'TOTVEGC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out

#############   gpppft   #############
varname_out = 'gpppft'
varname_in = 'GPP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out

#############   npppft   #############
varname_out = 'npppft'
varname_in = 'NPP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out

#############   npppft   #############
varname_out = 'nbppft'
varname_in = 'NBP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out


#############   tskinpft   #############
varname_out = 'tskinpft'
varname_in = 'TV'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):    
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out


#############   theightpft   #############
varname_out = 'theightpft'
varname_in = 'HTOP'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
    np.ma.set_fill_value(data_out, -99999.)
    for pft_i in range(npft):
        #
        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
        clobber(filename_out)
        file_out = Nio.open_file(filename_out, 'c')
        file_out.create_dimension('lat', JM)
        file_out.create_dimension('lon', IM)
        file_out.create_dimension('time', ntime_monthly)
        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
        file_timevarout = file_out.create_variable('time', 'f', ('time',))
        file_latvarout[:] = lats[:]
        file_lonvarout[:] = lons[:]
        file_timevarout[:] = time[:]
        for i, att in enumerate(lats.attributes):
            setattr(file_out.variables['lat'],att,lats.attributes[att])
        for i, att in enumerate(lons.attributes):
            setattr(file_out.variables['lon'],att,lons.attributes[att])
        for i, att in enumerate(time.attributes):
            setattr(file_out.variables['time'],att,time.attributes[att])
        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
#         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
#         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
        file_out.close()
    del data_out


#############   irripft #############
#varname_out = 'irripft'
#varname_in = 'QIRRIG'
#unit_conversion = 1.
#try:
#    list_index = vars_out.index(varname_out)
#except:
#    list_index = -1
#for exp_i in range(len(exp_list)):
#    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:,:] * unit_conversion
#    np.ma.set_fill_value(data_out, -99999.)
#    for pft_i in range(npft):
#        #
#        filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out+'_PFT_'+"%02d" % (pft_i+1) + '.nc'
#        clobber(filename_out)
#        file_out = Nio.open_file(filename_out, 'c')
#        file_out.create_dimension('lat', JM)
#        file_out.create_dimension('lon', IM)
#        file_out.create_dimension('time', ntime_monthly)
#        file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
#        file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
#        file_timevarout = file_out.create_variable('time', 'f', ('time',))
#        file_latvarout[:] = lats[:]
#        file_lonvarout[:] = lons[:]
#        file_timevarout[:] = time[:]
#        for i, att in enumerate(lats.attributes):
#            setattr(file_out.variables['lat'],att,lats.attributes[att])
#        for i, att in enumerate(lons.attributes):
#            setattr(file_out.variables['lon'],att,lons.attributes[att])
#        for i, att in enumerate(time.attributes):
#            setattr(file_out.variables['time'],att,time.attributes[att])
#        setattr(file_out,'pft_name_'+"%02d" % (pft_i+1),pftname[pft_i])
#        varname_out_ext = varname_out+'_PFT_'+"%02d" % (pft_i+1)
#        file_varout = file_out.create_variable(varname_out_ext, 'f', ('time', 'lat', 'lon'))
##         file_varout[:] = data_out[pft_i, :, :, :].astype('float32')
#        file_varout[:] = data_out[:, pft_i, :, :].astype('float32')
##         for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
##             setattr(file_out.variables[varname_out_ext],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
#        setattr(file_out.variables[varname_out_ext],'Units',units_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'Long_name',long_name_out_list[list_index])
#        setattr(file_out.variables[varname_out_ext],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
#        setattr(file_out.variables[varname_out_ext],'CLM_orig_varname',varname_in)
#        file_out.close()
#    del data_out


