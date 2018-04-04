# 3d_recon

* Functions

  - reconstruct 3d model from the series of 2d images.
    + mesh and Point cloud.
  ```
  User can see the both model using the viewer.
  Don't need to show simultaneously.
  ```
  
  - generate stitched image(orthomosaic).  
  - generate DEM(Digital elevation Model).(Probably from the 3d model mesh)
    + we can provide this with orthomosaic like how Pix4d does.
  - map
    + show orthomosaic and DEM on the actual map(ie. Google Maps)
    + CAD Overlay(not familiar).
  
  ```
  User see the orthomosaic and DEM on the Map(Google).
  ```
  - marker and annotation function.
  - measurment
    + measure certain length in the 3d model. (think about density of the 3d model, or rely on the 3d model viewer)
    + measure certain 2d area. (how to set the plane...? can we provide the curved plane?)
    + measure a volume of an area. (how to set the base plane? what if it is not just convex)
  ```
  marker can be put on 2d and 3d both.
  measuring will be performed only on the 3d model using mouse.  
  annotation saves markers and measurments. User can edit annotation's name, description.
  annotation have a visibility option.
  ```
 
  - File
    + mesh
    + point cloud
    + DEM
    + input images
    + orthomosaic  
  
  
  - Afterward
    + Calender
    + Find images which contain specific point. (Inspection)
