### Instructions for running SPFEAS_ZONAL locally

1. Add the sample tif to the **spfeas_in** folder.
2. Run **./execute_locally.sh**

The ** ./execute_locally.sh ** script removes the **temp** directory
if it exists. It then runs *docker-compose* against the **docker-compose.yml**
file. This file defines two services run in sequence.
The first is a custom build of **spfeas** followed by **spfeas_zonal**. The
**spfeas_zonal** process waits until the **spfeas** process has
written its status output file.  Input and output directories are specified as docker bind mounts in the
compose file. Outputs from both processes will be written to **./temp** directory.

#### Docker bind mounts used.

* **./spfeas_in** configured as bind mount to */mnt/work/input* for the **spfeas** process.
* **./temp** configured as a bind mount to */mnt/work/output* for the **spfeas** process.
* **./test_shape** configured as a bind mount to */mnt/shape* for the **spfeas_zonal** process.
* **./temp** configured as a bind mount to */mnt/work/input* for the **spfeas_zonal** process.
* **./temp** configured as a bind mount to */mnt/work/output* for the **spfeas_zonal** process.


This has been successfully tested using the **057523831010_01_assembly_clip.tif** file.
