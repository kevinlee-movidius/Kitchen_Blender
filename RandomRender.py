#!/usr/bin/python
import bpy
import random
from random import randint

camera = "Camera"


for frame in range(0,10):

    object =  bpy.data.objects[camera]
    object.select = True

#change location of object 
    bpy.context.object.location[0] = random.uniform(-2.6,4.5)
    bpy.context.object.location[1] = random.uniform(-3.7,3.2)
    bpy.context.object.location[2] = random.uniform(0.8,2.4)

    bpy.context.object.rotation_euler[2] = random.uniform(0,6.28319)

    bpy.data.scenes['Scene'].render.filepath = '/home/leek/Kitchen/rightcam_0.15m/' + str(frame).zfill(6) +'.jpg'
    bpy.ops.render.render( write_still=True ) 

    bpy.context.object.location[0] = bpy.context.object.location[0] - 0.15

    bpy.data.scenes['Scene'].render.filepath = '/home/leek/Kitchen/leftcam_0.15m/'+ str(frame).zfill(6) +'.jpg'
    bpy.ops.render.render( write_still=True ) 


# Set up rendering of depth map:
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

# clear default nodes
    for n in tree.nodes:
        tree.nodes.remove(n)

# create input render layer node
    rl = tree.nodes.new('CompositorNodeRLayers')

    map = tree.nodes.new(type="CompositorNodeMapValue")
# Size is chosen kind of arbitrarily, try out until you're satisfied with resulting depth map.
    map.size = [0.05]
    map.use_min = True
    map.min = [0]
    map.use_max = True
    map.max = [255]
    links.new(rl.outputs[2], map.inputs[0])

#invert = tree.nodes.new(type="CompositorNodeInvert")
#links.new(map.outputs[0], invert.inputs[1])

# The viewer can come in handy for inspecting the results in the GUI
    depthViewer = tree.nodes.new(type="CompositorNodeViewer")
    links.new(map.outputs[0], depthViewer.inputs[0])
# Use alpha from input.
    links.new(rl.outputs[1], depthViewer.inputs[1])

# create a file output node and set the path
    fileOutput = tree.nodes.new(type="CompositorNodeOutputFile")
    fileOutput.base_path = "/home/leek/Kitchen/depth_map/"

    links.new(map.outputs[0], fileOutput.inputs[0])
    bpy.context.scene.frame_current = frame + 1 

