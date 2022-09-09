#import Nio
import numpy as np
import Nio 
import glob

trendy='TRENDY2022'
sim='S3'


def clobber(filename):
    try:
        print('replacing file: '+filename)
        os.remove(filename)
    except:
        print('file does not exist: '+filename)
    

def monthly_to_annual(x, axis=0, nmonths=12, calendar="noleap"):
    """convert monthly to annual data. this keeps units constant"""
    ndims = len(x.shape)
    if type(x) == type(np.ma.masked_all([1])):
        masked=True
    else:
        masked=False
    #
    if calendar=='noleap' and nmonths ==12:
        monthlength = np.array([31.,28.,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.])
    elif calendar == None and nmonths == 12:
        monthlength = np.array([30.,30.,30.,30.,30.,30.,30.,30.,30.,30.,30.,30.])
    else:
        raise NotImplementedError
    #
    ntim = x.shape[axis]
    nyears = ntim//nmonths
    #
    if ndims == 1:
        if not masked:
            annual_x = np.zeros(nyears)
        else:
            annual_x = np.ma.masked_all(nyears)
        for i in range(nyears):
            annual_x[i] = (x[i*nmonths:(i+1)*nmonths] * monthlength).sum() / monthlength.sum()
        return annual_x
    elif ndims == 2:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,2)
        n_dim1 = x_rot.shape[0]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1])
        for i in range(nyears):
            annual_x[i,:] = (x_rot[:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=1) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        return annual_x
    elif ndims == 3:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,3)
        n_dim1 = x_rot.shape[0]
        n_dim2 = x_rot.shape[1]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1,n_dim2])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1,n_dim2])            
        for i in range(nyears):
            annual_x[i,:,:] = (x_rot[:,:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=2) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        elif axis == 2:
            annual_x = np.rotate(annual_x,0,3)
        return annual_x
    elif ndims == 4:
        # rotate time axis to end
        x_rot = np.rollaxis(x,axis,4)
        n_dim1 = x_rot.shape[0]
        n_dim2 = x_rot.shape[1]
        n_dim3 = x_rot.shape[2]
        if not masked:
            annual_x = np.zeros([nyears,n_dim1,n_dim2,n_dim3])
        else:
            annual_x = np.ma.masked_all([nyears,n_dim1,n_dim2,n_dim3])            
        for i in range(nyears):
            annual_x[i,:,:,:] = (x_rot[:,:,:,i*nmonths:(i+1)*nmonths] * monthlength).sum(axis=3) / monthlength.sum()
        # rotate time axis back to original position
        if axis == 1:
            annual_x = np.rotate(annual_x,0,2)
        elif axis == 2:
            annual_x = np.rotate(annual_x,0,3)
        elif axis == 3:
            annual_x = np.rotate(annual_x,0,4)
        return annual_x
    else:
        raise NotImplementedError
    
print('starting to read variables')

read_input_file = True
if read_input_file:
    vars_in = ['QRUNOFF', 'QVEGT', 'QVEGE', 'QSOIL', 'FSH', 'TSA', 'TOTVEGC', 'TOTLITC', 'TOTSOMC', 'GPP', 'AR', 'NPP', 'HR', 'COL_FIRE_CLOSS', 'LAND_USE_FLUX', 'NBP', 'FCEV', 'FGEV', 'FCTR', 'FSR', 'FIRA', 'FGR', 'SNOWDP', 'SNOWLIQ', 'SNOWICE', 'LITFALL', 'LEAFC', 'WOODC', 'DEADCROOTC', 'FROOTC', 'LIVECROOTC', 'CWDC', 'FAREA_BURNED', 'TOT_WOODPRODC', 'TOTSOMC_1m', 'TLAI', 'NFIX', 'FFIX_TO_SMINN','NDEP_TO_SMINN', 'NET_NMIN', 'SMINN_TO_PLANT', 'SMIN_NO3_LEACHED', 'SMIN_NO3_RUNOFF', 'DENIT', 'TOTLITN', 'TOTSOMN', 'TOTVEGN', 'TOTLITN', 'TOT_WOODPRODN', 'FSDS', 'RAIN', 'SNOW','CROPPROD1C_LOSS','DWT_CONV_CFLUX','TOT_WOODPRODC_LOSS','TOTSOILLIQ','TOTSOILICE']

    datadir_in = '/glade/campaign/asp/djk2120/'+trendy+'/'+sim+'/lnd/proc/tseries/month_1/'
    
    datadir_out = '/glade/campaign/asp/djk2120/'+trendy+'/'+sim+'/lnd/proc/trendy/'

    file = glob.glob(datadir_in+'*h0*NBP*.nc')[0]
    f1,f2 = file.split('NBP')

    filein_list_exp2 = []

    for var_i, varname in enumerate(vars_in):
        print('starting var '+varname)
        filename=f1 + varname + f2
        print('filename: '+filename)
        filein_list_exp2.append(Nio.open_file(filename))
        locals()[varname+'_exp2'] = filein_list_exp2[len(filein_list_exp2)-1].variables[varname]
        #
        if var_i == 0:
            lats = filein_list_exp2[len(filein_list_exp2)-1].variables['lat']
            lons = filein_list_exp2[len(filein_list_exp2)-1].variables['lon']
            time = filein_list_exp2[len(filein_list_exp2)-1].variables['time']
            ntime_monthly = len(time[:])
            ntime_annual = ntime_monthly // 12
            JM = len(lats[:])
            IM = len(lons[:])

    vars_out = ['mrso', 'mrro', 'evapotrans', 'sh', 'tas', 'cVeg', 'cLitter', 'cSoil', 'gpp', 'ra', 'npp', 'rh', 'fFire', 'fLuc', 'nbp', 'landCoverFrac', 'lai', 'tsl', 'msl', 'evspsblveg', 'evspsblsoi', 'tran', 'swup', 'lwup', 'ghflx', 'snow_depth', 'swe', 'fGrazing', 'fHarvest', 'fVegLitter', 'fLitterSoil', 'fVegSoil', 'cLeaf', 'cWood', 'cRoot', 'cCwd', 'burntArea', 'cProduct', 'dlai', 'fBNF','fNdep','fNnetmin', 'fNup', 'fNloss', 'nSoil', 'nVeg', 'nLitter', 'nProduct', 'rsds', 'pr']

    exp_list = ['_exp2']

    exp_outputname_list = ['CLM5.0_'+sim+'_']

    units_out_list = ['kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'W m-2', 'K', 'kg m-2', 'kg m-2', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'None', 'None', 'K', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'W m-2', 'W m-2', 'W m-2', 'm', 'kg m-2', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2', 'kg m-2', 'kg m-2', 'kg m-2', '%', 'kg m-2', 'None', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2 s-1', 'kg m-2', 'kg m-2', 'kg m-2', 'kg m-2', 'W m-2', 'kg m-2 s-1']



    long_name_out_list = ['Total Soil Moisture Content', 'Total Runoff', 'Total Evapo-Transpiration', 'Sensible heat flux', 'Surface temperature', 'Carbon in Vegetation', 'Carbon in Above-ground Litter Pool', 'Carbon in Soil (including below-ground litter)', 'Gross Primary Production', 'Autotrophic (Plant) Respiration', 'Net Primary Production', 'Heterotrophic Respiration', 'CO2 Emission from Fire', 'CO2 Flux to Atmosphere from Land Use Change', 'Net Biospheric Production', 'Fractional Land Cover of PFT', 'Leaf Area Index', 'Temperature of Soil', 'Moisture of Soil', 'Evaporation from Canopy', 'Water Evaporation from Soil', 'Transpiration', 'Shortwave up radiation', 'Longwave up radiation', 'Ground heat flux', 'Snow Depth ', 'Snow Water Equivalent ', 'CO2 Flux to Atmosphere from Grazing', 'CO2 Flux to Atmosphere from Crop Harvesting', 'Total Carbon Flux from Vegetation to Litter', 'Total Carbon Flux from Litter to Soil', 'Total Carbon Flux from Vegetation Directly to Soil', 'Carbon in Leaves', 'Carbon in Wood', 'Carbon in Roots', 'Carbon in Coarse Woody Debris', 'Burnt Area Fraction', 'Carbon in Products of Land Use Change', 'Leaf Area Index Daily', 'Biological Nitrogen Fixation','Nitrogen Deposition', 'Net Nitrogen Mineralization','Nitrogen Uptake of Vegetation', 'Total Ecosystem Nitrogen Loss', 'Nitrogen in Soil (including belowground litter)', 'Nitrogen in Vegetation', 'Nitrogen in Aboveground Litter Pool', 'Nitrogen in Products of Land Use Change', 'Surface Downwelling Shortwave Radiation', 'Precipitation']

#####DLL NOTE: end edits
    
heat_vaporization_h2o = 2.501e6 ## j / kg

    
#############   mrro   #############
varname_out = 'mrro'
varname_in = ['QRUNOFF']
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out

##############   evapotrans   #############
varname_out = 'evapotrans'
varname_in = ['QVEGT', 'QVEGE', 'QSOIL']
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out

##############   mrso   #############
varname_out = 'mrso'
varname_in = ['TOTSOILLIQ', 'TOTSOILICE']
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


#############   cRoot   #############
varname_out = 'cRoot'
varname_in = ['DEADCROOTC', 'FROOTC', 'LIVECROOTC']
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out

#############   cSoil   #############
varname_out = 'cSoil'
varname_in = ['TOTLITC', 'TOTSOMC']
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


#############   fLuc   #############
varname_out = 'fLuc'
#varname_in = 'LAND_USE_FLUX'
varname_in = ['DWT_CONV_CFLUX', 'TOT_WOODPRODC_LOSS']
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
#DLL start edits
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out

#############   fBNF  #############
varname_out = 'fBNF' 
varname_in = ['NFIX', 'FFIX_TO_SMINN'] 
unit_conversion = 1.e-3 
try:    
    list_index = vars_out.index(varname_out)
except: 
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc' 
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon')) 
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:] 
    file_lonvarout[:] = lons[:] 
    file_timevarout[:] = time[:] 
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


################################################################################   singleton variables


#############   npp   #############
varname_out = 'npp'
varname_in = 'NPP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   tas   #############
varname_out = 'tas'
varname_in = 'TSA'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   gpp   #############
varname_out = 'gpp'
varname_in = 'GPP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   ra   #############
varname_out = 'ra'
varname_in = 'AR'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   rh   #############
varname_out = 'rh'
varname_in = 'HR'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   fFire   #############
varname_out = 'fFire'
varname_in = 'COL_FIRE_CLOSS'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out



#############   nbp   #############
varname_out = 'nbp'
varname_in = 'NBP'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out




#############   evspsblveg   #############
varname_out = 'evspsblveg'
varname_in = 'QVEGE'
unit_conversion = 1. 
#varname_in = 'FCEV'
#unit_conversion = 1. / heat_vaporization_h2o
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

### DLL Note: updated to use equivalent variable
#############   evspsblsoi   #############
varname_out = 'evspsblsoi'
varname_in = 'QSOIL'
unit_conversion = 1. 
#varname_in = 'FGEV'
#unit_conversion = 1. / heat_vaporization_h2o
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

### DLL Note: updated to use equivalent variable
#############   tran   #############
varname_out = 'tran'
varname_in = 'QVEGT'
unit_conversion = 1. 
#varname_in = 'FCTR'
#unit_conversion = 1. / heat_vaporization_h2o
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out



################################################################################  annual fields
    
#############   cVeg   #############
varname_out = 'cVeg'
varname_in = 'TOTVEGC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


  
#############   cLitter   #############
varname_out = 'cLitter'
varname_in = 'TOTLITC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


  

#############   cLeaf   #############
varname_out = 'cLeaf'
varname_in = 'LEAFC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   cWood   #############
varname_out = 'cWood'
varname_in = 'WOODC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   cCwd   #############
varname_out = 'cCwd'
varname_in = 'CWDC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out



  
#############   cProduct   #############
varname_out = 'cProduct'
varname_in = 'TOT_WOODPRODC'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

    

#############   burntArea   #############
varname_out = 'burntArea'
varname_in = 'FAREA_BURNED'

unit_conversion = 86400. * 30.  ## per sec -> per month
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = (locals()[varname_in+exp_list[exp_i]][:,:,:]) * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    print(data_out.shape)
    print(data_out.dtype)
    print(file_varout[:].shape)
    print(file_varout[:].dtype)
    file_varout[:] = data_out[:]
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


    
#############   lai   #############
varname_out = 'lai'
varname_in = 'TLAI'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#### DLL Note: New variables added #### 

#### New Physical Variables ####

#############   rsds   #############
varname_out = 'rsds'
varname_in = 'FSDS'
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   pr   #############
varname_out = 'pr'
varname_in = ['RAIN', 'SNOW']
unit_conversion = 1.
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


#### New N pools ####

#############   nSoil   #############
varname_out = 'nSoil'
varname_in = ['TOTLITN', 'TOTSOMN']
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


#############   nVeg   #############
varname_out = 'nVeg'
varname_in = 'TOTVEGN'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   nLitter   #############
varname_out = 'nLitter'
varname_in = 'TOTLITN'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out


#############   nProduct   #############
varname_out = 'nProduct'
varname_in = 'TOT_WOODPRODN'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][::12,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_annual)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[::12]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out



#### New N Fluxes ####

#############   fNloss   #############
varname_out = 'fNloss'
varname_in = ['SMIN_NO3_LEACHED', 'SMIN_NO3_RUNOFF', 'DENIT']
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    for summation_i in range(len(varname_in)):
        if summation_i == 0:
            full_varname_string = varname_in[summation_i]
            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
        else:
            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:] * unit_conversion
    #
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out


#############   fNdep  #############
varname_out = 'fNdep'
varname_in = 'NDEP_TO_SMINN'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   fNnetmin  #############
varname_out = 'fNnetmin'
varname_in = 'NET_NMIN'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   fNup  #############
varname_out = 'fNup'
varname_in = 'SMINN_TO_PLANT'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
    file_out.close()
    del data_out

#############   fLitterSoil   #############
varname_out = 'fLitterSoil'
varname_in = 'LITFALL' 
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out

#############   fHarvest   #############
varname_out = 'fHarvest'
varname_in = 'CROPPROD1C_LOSS'
unit_conversion = 1.e-3
try:
    list_index = vars_out.index(varname_out)
except:
    list_index = -1
#Start DLL edits
for exp_i in range(len(exp_list)):
    data_out = locals()[varname_in+exp_list[exp_i]][:,:,:] * unit_conversion
    #       
    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'

#for exp_i in range(len(exp_list)):
#    for summation_i in range(len(varname_in)):
#        if summation_i == 0:
#            full_varname_string = varname_in[summation_i]
#            data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
#        else:
#            full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
#            data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:]
#    #
#    filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
#End DLL edits
    clobber(filename_out)
    file_out = Nio.open_file(filename_out, 'c')
    file_out.create_dimension('lat', JM)
    file_out.create_dimension('lon', IM)
    file_out.create_dimension('time', ntime_monthly)
    file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lat', 'lon'))
    file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
    file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
    file_timevarout = file_out.create_variable('time', 'f', ('time',))
    np.ma.set_fill_value(data_out, -99999.)
    file_varout[:] = data_out
    file_latvarout[:] = lats[:]
    file_lonvarout[:] = lons[:]
    file_timevarout[:] = time[:]
    for i, att in enumerate(lats.attributes):
        setattr(file_out.variables['lat'],att,lats.attributes[att])
    for i, att in enumerate(lons.attributes):
        setattr(file_out.variables['lon'],att,lons.attributes[att])
    for i, att in enumerate(time.attributes):
        setattr(file_out.variables['time'],att,time.attributes[att])
    for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
        setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
    setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
    setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
    setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
    setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
    file_out.close()
    del data_out





# ###### THESE DON'T WORK, even on big machine.  try this instead at the command line:

# ncrename -D 2 -v TSOI,tsl S0/TRENDY2020_S0_constant.clm2.h0.TSOI.170001-201912.nc CLM5.0_S0_tsl.nc
# ncrename -D 2 -v TSOI,tsl S1/TRENDY2020_S1_CO2.clm2.h0.TSOI.170001-201912.nc CLM5.0_S1_tsl.nc
# ncrename -D 2 -v TSOI,tsl S2/TRENDY2020_S2_CO2Climate.clm2.h0.TSOI.170001-201912.nc CLM5.0_S2_tsl.nc
# ncrename -D 2 -v TSOI,tsl S3/TRENDY2020_S3_CO2ClimateLUC.clm2.h0.TSOI.170001-201912.nc CLM5.0_S3_tsl.nc

# ncrename -v SOILICE,msl S0/TRENDY2020_S0_constant.clm2.h0.SOILICE.170001-201912.nc CLM5.0_S0_msl_ice.nc
# ncrename -v SOILICE,msl S1/TRENDY2020_S1_CO2.clm2.h0.SOILICE.170001-201912.nc CLM5.0_S1_msl_ice.nc
# ncrename -v SOILICE,msl S2/TRENDY2020_S2_CO2Climate.clm2.h0.SOILICE.170001-201912.nc CLM5.0_S2_msl_ice.nc
# ncrename -v SOILICE,msl S3/TRENDY2020_S3_CO2ClimateLUC.clm2.h0.SOILICE.170001-201912.nc CLM5.0_S3_msl_ice.nc

# ncrename -v SOILLIQ,msl S0/TRENDY2020_S0_constant.clm2.h0.SOILLIQ.170001-201912.nc CLM5.0_S0_msl_liq.nc
# ncrename -v SOILLIQ,msl S1/TRENDY2020_S1_CO2.clm2.h0.SOILLIQ.170001-201912.nc CLM5.0_S1_msl_liq.nc
# ncrename -v SOILLIQ,msl S2/TRENDY2020_S2_CO2Climate.clm2.h0.SOILLIQ.170001-201912.nc CLM5.0_S2_msl_liq.nc
# ncrename -v SOILLIQ,msl S3/TRENDY2020_S3_CO2ClimateLUC.clm2.h0.SOILLIQ.170001-201912.nc CLM5.0_S3_msl_liq.nc

# ncbo --op_typ=+ CLM5.0_S0_msl_ice.nc CLM5.0_S0_msl_liq.nc CLM5.0_S0_msl.nc
# ncbo --op_typ=+ CLM5.0_S1_msl_ice.nc CLM5.0_S1_msl_liq.nc CLM5.0_S1_msl.nc
# ncbo --op_typ=+ CLM5.0_S2_msl_ice.nc CLM5.0_S2_msl_liq.nc CLM5.0_S2_msl.nc
# ncbo --op_typ=+ CLM5.0_S3_msl_ice.nc CLM5.0_S3_msl_liq.nc CLM5.0_S3_msl.nc


# #############   tsl   #############
# varname_out = 'tsl'
# varname_in = 'TSOI'
# unit_conversion = 1.
# try:
#     list_index = vars_out.index(varname_out)
# except:
#     list_index = -1
# for exp_i in range(len(exp_list)):
#     #
#     filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
#     clobber(filename_out)
#     file_out = Nio.open_file(filename_out, 'c')
#     file_out.create_dimension('lat', JM)
#     file_out.create_dimension('lon', IM)
#     file_out.create_dimension('lev', nlev)
#     file_out.create_dimension('time', ntime_monthly)
#     file_varout = file_out.create_variable(varname_out, 'f', ('time', 'lev', 'lat', 'lon'))
#     file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
#     file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
#     file_timevarout = file_out.create_variable('time', 'f', ('time',))
#     file_levvarout = file_out.create_variable('lev', 'f', ('lev',))
#     print(file_varout[:,:,:,:].dtype)
#     print(file_varout[:,:,:,:].shape)
#     print(locals()[varname_in+exp_list[exp_i]][:,:,:,:].dtype)
#     print(locals()[varname_in+exp_list[exp_i]][:,:,:,:].shape)    
#     file_varout[:] = locals()[varname_in+exp_list[exp_i]][:,:,:,:]
#     file_latvarout[:] = lats[:]
#     file_lonvarout[:] = lons[:]
#     file_timevarout[:] = time[:]
#     file_levvarout[:] = lev[:]
#     for i, att in enumerate(lats.attributes):
#         setattr(file_out.variables['lat'],att,lats.attributes[att])
#     for i, att in enumerate(lons.attributes):
#         setattr(file_out.variables['lon'],att,lons.attributes[att])
#     for i, att in enumerate(time.attributes):
#         setattr(file_out.variables['time'],att,time.attributes[att])
#     for i, att in enumerate(lev.attributes):
#         setattr(file_out.variables['lev'],att,lev.attributes[att])
#     for i, att in enumerate(locals()[varname_in+exp_list[exp_i]].attributes):
#         setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in+exp_list[exp_i]].attributes[att])
#     setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
#     setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
#     setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
#     setattr(file_out.variables[varname_out],'CLM_orig_varname',varname_in)
#     file_out.close()
  
# #############   msl   #############
# varname_out = 'msl'
# varname_in = ['SOILLIQ', 'SOILICE']
# unit_conversion = 1.
# try:
#     list_index = vars_out.index(varname_out)
# except:
#     list_index = -1
# for exp_i in range(len(exp_list)):
#     for summation_i in range(len(varname_in)):
#         if summation_i == 0:
#             full_varname_string = varname_in[summation_i]
#             data_out = locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:,:]
#         else:
#             full_varname_string = full_varname_string + ' + ' + varname_in[summation_i]
#             data_out = data_out + locals()[varname_in[summation_i]+exp_list[exp_i]][:,:,:,:]
#     #
#     filename_out = datadir_out + exp_outputname_list[exp_i] + varname_out + '.nc'
#     clobber(filename_out)
#     file_out = Nio.open_file(filename_out, 'c')
#     file_out.create_dimension('lat', JM)
#     file_out.create_dimension('lon', IM)
#     file_out.create_dimension('time', ntime_monthly)
#     file_out.create_dimension('lev', nlev)
#     file_varout = file_out.create_variable(varname_out, 'f', ('time','lev', 'lat', 'lon'))
#     file_latvarout = file_out.create_variable('lat', 'f', ('lat',))
#     file_lonvarout = file_out.create_variable('lon', 'f', ('lon',))
#     file_timevarout = file_out.create_variable('time', 'f', ('time',))
#     file_levvarout = file_out.create_variable('lev', 'f', ('lev',))
#     np.ma.set_fill_value(data_out, -99999.)
#     file_varout[:] = data_out.astype('float32')
#     file_latvarout[:] = lats[:]
#     file_lonvarout[:] = lons[:]
#     file_timevarout[:] = time[:]
#     file_levvarout[:] = lev[:]
#     for i, att in enumerate(lats.attributes):
#         setattr(file_out.variables['lat'],att,lats.attributes[att])
#     for i, att in enumerate(lons.attributes):
#         setattr(file_out.variables['lon'],att,lons.attributes[att])
#     for i, att in enumerate(time.attributes):
#         setattr(file_out.variables['time'],att,time.attributes[att])
#     for i, att in enumerate(lev.attributes):
#         setattr(file_out.variables['lev'],att,lev.attributes[att])
#     for i, att in enumerate(locals()[varname_in[0]+exp_list[exp_i]].attributes):
#         setattr(file_out.variables[varname_out],'CLM_orig_attr_'+att,locals()[varname_in[0]+exp_list[exp_i]].attributes[att])
#     setattr(file_out.variables[varname_out],'Units',units_out_list[list_index])
#     setattr(file_out.variables[varname_out],'Long_name',long_name_out_list[list_index])
#     setattr(file_out.variables[varname_out],'CLM-TRENDY_unit_conversion_factor',unit_conversion)
#     setattr(file_out.variables[varname_out],'CLM_orig_varname',full_varname_string)
#     file_out.close()
