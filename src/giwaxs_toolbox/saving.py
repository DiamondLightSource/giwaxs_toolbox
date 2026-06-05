# def save_1D_integration(tiffile, qbins, qmin, qmax, chi_pos, chi_width, maskfile, ponifile, incident_angle, out_dir):
#     import_poni(ponifile)
#     update_pg_I07(incident_angle=incident_angle, maskfile=maskfile, mask=True)
    
#     img = fabio.open(tiffile).data
#     intensity, q = integrate1d(img, qbins, qmin, qmax, chi_pos, chi_width)
    
#     tiffname = Path(tiffile).stem
    
#     # Save single 1D text file
#     df_single = pd.DataFrame({"q A-1": q, "Intensity": intensity})
#     out_txt = os.path.join(out_dir, f"{tiffname}_1Dintegration_chi{chi_pos}_{chi_width}.txt")
#     df_single.to_csv(out_txt, sep='\t', index=False)
    
#     return q, intensity, tiffname

# def save_GIWAXS(tiffile, outfile,qbins=1500,qxy_min=-3, qxy_max=3,qz_min=0, qz_max=3,vmin=2, 
#                 vmax=200,polarization_factor=1, xmin=-2, xmax=2, ymin=0, ymax=2.2,dpi=600):

#     img = fabio.open(tiffile).data
#     intensity, qxy, qz = pygix_transform_global(
#         img, qbins,
#         default_range=False,
#         qxy_min=qxy_min, qxy_max=qxy_max,
#         qz_min=qz_min, qz_max=qz_max,
#         polarization_factor=polarization_factor
#     )

#     intensity_flipped = np.fliplr(np.flipud(intensity))

#     plot_GIWAXS(intensity_flipped, qxy, qz,
#                 vmin, vmax, outfile,
#                 dpi=dpi, saving=True,
#                 xmin=xmin, xmax=xmax,
#                 ymin=ymin, ymax=ymax)


# def save_giwaxs_2d(outfile):
#     plt.savefig(outfile + ".png", bbox_inches='tight')
#     plt.savefig(outfile + ".pdf", bbox_inches='tight')