bl_info = {
	"name": "VF Update Images",
	"author": "John Einselen - Vectorform LLC",
	"version": (0, 3),
	"blender": (3, 2, 0),
	"location": "Image Editor > Image > Update Images",
	"description": "Reloads images and updates settings based on file naming patterns",
	"warning": "inexperienced developer, use at your own risk",
	"doc_url": "https://github.com/jeinselenVF/VF-BlenderUpdateImages",
	"tracker_url": "https://github.com/jeinselenVF/VF-BlenderUpdateImages/issues",
	"category": "User Interface"}

# Helped by the following resources:
# https://blender.stackexchange.com/questions/44836/reloading-multiple-images
# https://docs.blender.org/api/current/bpy.types.Image.html#bpy.types.Image

import bpy

###########################################################################
# Update images

class VF_Update_Images(bpy.types.Operator):
	bl_idname = "vfupdateimages.offset"
	bl_label = "Update All Images"
	bl_icon = "RENDERLAYERS"
	bl_description = "Process all images, updating colour space and alpha channel settings based on name patterns, and reloading any images that don't have unsaved changes in Blender"
	bl_options = {'REGISTER', 'UNDO'}
	
	reload: bpy.props.BoolProperty()
	format: bpy.props.BoolProperty()
	
	def execute(self, context):
		for image in bpy.data.images:
			# Reload all image files
			if self.reload:
				# Prevent reloading of files that have unsaved changes in Blender
				if not image.is_dirty:
					image.reload()
			
			# Format all image files
			if self.format:
				# Update file settings based on file name matches
				imageName = image.name.lower()
				if bpy.context.preferences.addons['VF_updateImages'].preferences.filter1_name.lower() in imageName:
					image.colorspace_settings.name = bpy.context.preferences.addons['VF_updateImages'].preferences.filter1_colorspace
					image.alpha_mode = bpy.context.preferences.addons['VF_updateImages'].preferences.filter1_alphamode
				elif bpy.context.preferences.addons['VF_updateImages'].preferences.filter2_name.lower() in imageName:
					image.colorspace_settings.name = bpy.context.preferences.addons['VF_updateImages'].preferences.filter2_colorspace
					image.alpha_mode = bpy.context.preferences.addons['VF_updateImages'].preferences.filter2_alphamode
				elif bpy.context.preferences.addons['VF_updateImages'].preferences.filter3_name.lower() in imageName:
					image.colorspace_settings.name = bpy.context.preferences.addons['VF_updateImages'].preferences.filter3_colorspace
					image.alpha_mode = bpy.context.preferences.addons['VF_updateImages'].preferences.filter3_alphamode
				elif bpy.context.preferences.addons['VF_updateImages'].preferences.filter4_name.lower() in imageName:
					image.colorspace_settings.name = bpy.context.preferences.addons['VF_updateImages'].preferences.filter4_colorspace
					image.alpha_mode = bpy.context.preferences.addons['VF_updateImages'].preferences.filter4_alphamode
				elif bpy.context.preferences.addons['VF_updateImages'].preferences.filter5_name.lower() in imageName:
					image.colorspace_settings.name = bpy.context.preferences.addons['VF_updateImages'].preferences.filter5_colorspace
					image.alpha_mode = bpy.context.preferences.addons['VF_updateImages'].preferences.filter5_alphamode
		return {'FINISHED'}

###########################################################################
# Replace images (file extension swap)

class VF_Switch_Extension_Settings(bpy.types.Operator):
	bl_idname = "vfswitchextensionsettings.offset"
	bl_label = "Switch File Extension Settings"
	bl_icon = "FILE_REFRESH"
	bl_description = "Process all images, updating colour space and alpha channel settings based on name patterns, and reloading any images that don't have unsaved changes in Blender"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		source = bpy.context.scene.vf_update_images_settings.file_extension_source
		target = bpy.context.scene.vf_update_images_settings.file_extension_target
		bpy.context.scene.vf_update_images_settings.file_extension_source = target
		bpy.context.scene.vf_update_images_settings.file_extension_target = source
		return {'FINISHED'}

class VF_Replace_Image_Extensions(bpy.types.Operator):
	bl_idname = "vfreplaceimageextensions.offset"
	bl_label = "Replace All Image Extensions"
	bl_icon = "FILE_REFRESH"
	bl_description = "Replace all images that match the source file extension (left) with files using the target file extension (right), assumes that files already exist in the file system"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		source = bpy.context.scene.vf_update_images_settings.file_extension_source
		target = bpy.context.scene.vf_update_images_settings.file_extension_target

		for image in bpy.data.images:
			# Prevent replacing files that have unsaved changes in Blender
			if not image.is_dirty:
				image.filepath = image.filepath.replace(source, target)
				image.name = image.name.replace(source, target)
#				image.reload()
		bpy.context.scene.vf_update_images_settings.file_extension_source = target
		bpy.context.scene.vf_update_images_settings.file_extension_target = source
		return {'FINISHED'}

###########################################################################
# Global user preferences and UI display

class UpdateImagesPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__

	# Global Variables
	enable_file_reload: bpy.props.BoolProperty(
		name="File Reload",
		description="Reloads all image files",
		default=True)
	enable_file_format: bpy.props.BoolProperty(
		name="File Format",
		description="Formats all image files using the specified filters",
		default=False)
	
	filter1_name: bpy.props.StringProperty(
		name="Filter Name",
		description="String to match in the image name",
		default="-color",
		maxlen=4096)
	filter1_colorspace: bpy.props.EnumProperty(
		name='Color Space',
		description='Set matching files to this color space',
		items=[
			('Filmic Log', 'Filmic Log', 'Filmic Log color space'),
			('Linear', 'Linear', 'Linear color space'),
			('Linear ACES', 'Linear ACES', 'Linear ACES color space'),
			('Linear ACEScg', 'Linear ACEScg', 'Linear ACEScg color space'),
			('Non-Color', 'Non-Color', 'Non-Color color space'),
			('Raw', 'Raw', 'Raw color space'),
			('sRGB', 'sRGB', 'sRGB color space'),
			('XYZ', 'XYZ', 'XYZ color space')
			],
		default='sRGB')
	filter1_alphamode: bpy.props.EnumProperty(
		name='Alpha Mode',
		description='Set matching files to this alpha mode',
		items=[
			('STRAIGHT', 'Straight', 'RGB channels are stored without association, but the alpha still operates as a mask'),
			('PREMUL', 'Premultiplied', 'RGB channels have been multiplied by the alpha'),
			('CHANNEL_PACKED', 'Channel Packed', 'Treat alpha as a fourth color channel without masking'),
			('NONE', 'None', 'Ignore alpha channel')
			],
		default='STRAIGHT')
	
	filter2_name: bpy.props.StringProperty(
		name="Filter Name",
		description="String to match in the image name",
		default="-orm",
		maxlen=4096)
	filter2_colorspace: bpy.props.EnumProperty(
		name='Color Space',
		description='Set matching files to this color space',
		items=[
			('Filmic Log', 'Filmic Log', 'Filmic Log color space'),
			('Linear', 'Linear', 'Linear color space'),
			('Linear ACES', 'Linear ACES', 'Linear ACES color space'),
			('Linear ACEScg', 'Linear ACEScg', 'Linear ACEScg color space'),
			('Non-Color', 'Non-Color', 'Non-Color color space (typically used for normal maps)'),
			('Raw', 'Raw', 'Raw color space'),
			('sRGB', 'sRGB', 'sRGB color space'),
			('XYZ', 'XYZ', 'XYZ color space')
			],
		default='Non-Color')
	filter2_alphamode: bpy.props.EnumProperty(
		name='Alpha Mode',
		description='Set matching files to this alpha mode',
		items=[
			('STRAIGHT', 'Straight', 'RGB channels are stored without association, but the alpha channel still operates as a mask'),
			('PREMUL', 'Premultiplied', 'RGB channels have been multiplied by the alpha channel as an embedded mask'),
			('CHANNEL_PACKED', 'Channel Packed', 'Treat the alpha as a fourth color channel without masking'),
			('NONE', 'None', 'Ignore alpha channel')
			],
		default='CHANNEL_PACKED')
	
	filter3_name: bpy.props.StringProperty(
		name="Filter Name",
		description="String to match in the image name",
		default="-normal",
		maxlen=4096)
	filter3_colorspace: bpy.props.EnumProperty(
		name='Color Space',
		description='Set matching files to this color space',
		items=[
			('Filmic Log', 'Filmic Log', 'Filmic Log color space'),
			('Linear', 'Linear', 'Linear color space'),
			('Linear ACES', 'Linear ACES', 'Linear ACES color space'),
			('Linear ACEScg', 'Linear ACEScg', 'Linear ACEScg color space'),
			('Non-Color', 'Non-Color', 'Non-Color color space (typically used for normal maps)'),
			('Raw', 'Raw', 'Raw color space'),
			('sRGB', 'sRGB', 'sRGB color space'),
			('XYZ', 'XYZ', 'XYZ color space')
			],
		default='Non-Color')
	filter3_alphamode: bpy.props.EnumProperty(
		name='Alpha Mode',
		description='Set matching files to this alpha mode',
		items=[
			('STRAIGHT', 'Straight', 'RGB channels are stored without association, but the alpha channel still operates as a mask'),
			('PREMUL', 'Premultiplied', 'RGB channels have been multiplied by the alpha channel as an embedded mask'),
			('CHANNEL_PACKED', 'Channel Packed', 'Treat the alpha as a fourth color channel without masking'),
			('NONE', 'None', 'Ignore alpha channel')
			],
		default='CHANNEL_PACKED')
	
	filter4_name: bpy.props.StringProperty(
		name="Filter Name",
		description="String to match in the image name",
		default="",
		maxlen=4096)
	filter4_colorspace: bpy.props.EnumProperty(
		name='Color Space',
		description='Set matching files to this color space',
		items=[
			('Filmic Log', 'Filmic Log', 'Filmic Log color space'),
			('Linear', 'Linear', 'Linear color space'),
			('Linear ACES', 'Linear ACES', 'Linear ACES color space'),
			('Linear ACEScg', 'Linear ACEScg', 'Linear ACEScg color space'),
			('Non-Color', 'Non-Color', 'Non-Color color space (typically used for normal maps)'),
			('Raw', 'Raw', 'Raw color space'),
			('sRGB', 'sRGB', 'sRGB color space'),
			('XYZ', 'XYZ', 'XYZ color space')
			],
		default='sRGB')
	filter4_alphamode: bpy.props.EnumProperty(
		name='Alpha Mode',
		description='Set matching files to this alpha mode',
		items=[
			('STRAIGHT', 'Straight', 'RGB channels are stored without association, but the alpha channel still operates as a mask'),
			('PREMUL', 'Premultiplied', 'RGB channels have been multiplied by the alpha channel as an embedded mask'),
			('CHANNEL_PACKED', 'Channel Packed', 'Treat the alpha as a fourth color channel without masking'),
			('NONE', 'None', 'Ignore alpha channel')
			],
		default='STRAIGHT')

	filter5_name: bpy.props.StringProperty(
		name="Filter Name",
		description="String to match in the image name",
		default="",
		maxlen=4096)
	filter5_colorspace: bpy.props.EnumProperty(
		name='Color Space',
		description='Set matching files to this color space',
		items=[
			('Filmic Log', 'Filmic Log', 'Filmic Log color space'),
			('Linear', 'Linear', 'Linear color space'),
			('Linear ACES', 'Linear ACES', 'Linear ACES color space'),
			('Linear ACEScg', 'Linear ACEScg', 'Linear ACEScg color space'),
			('Non-Color', 'Non-Color', 'Non-Color color space (typically used for normal maps)'),
			('Raw', 'Raw', 'Raw color space'),
			('sRGB', 'sRGB', 'sRGB color space'),
			('XYZ', 'XYZ', 'XYZ color space')
			],
		default='sRGB')
	filter5_alphamode: bpy.props.EnumProperty(
		name='Alpha Mode',
		description='Set matching files to this alpha mode',
		items=[
			('STRAIGHT', 'Straight', 'RGB channels are stored without association, but the alpha channel still operates as a mask'),
			('PREMUL', 'Premultiplied', 'RGB channels have been multiplied by the alpha channel as an embedded mask'),
			('CHANNEL_PACKED', 'Channel Packed', 'Treat the alpha as a fourth color channel without masking'),
			('NONE', 'None', 'Ignore alpha channel')
			],
		default='STRAIGHT')
	
	# User Interface
	def draw(self, context):
		layout = self.layout
		
		layout.prop(self, "enable_file_reload")
		layout.prop(self, "enable_file_format")
		
		grid = layout.grid_flow(row_major=True, columns=2, even_columns=False, even_rows=False, align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_format:
			grid.enabled = False
		
		grid.prop(self, "filter1_name", text='')
		row1 = grid.row(align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.filter1_name:
			row1.enabled = False
		row1.prop(self, "filter1_colorspace", text='')
		row1.prop(self, "filter1_alphamode", text='')
		
		grid.prop(self, "filter2_name", text='')
		row2 = grid.row(align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.filter2_name:
			row2.enabled = False
		row2.prop(self, "filter2_colorspace", text='')
		row2.prop(self, "filter2_alphamode", text='')
		
		grid.prop(self, "filter3_name", text='')
		row3 = grid.row(align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.filter3_name:
			row3.enabled = False
		row3.prop(self, "filter3_colorspace", text='')
		row3.prop(self, "filter3_alphamode", text='')
		
		grid.prop(self, "filter4_name", text='')
		row4 = grid.row(align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.filter4_name:
			row4.enabled = False
		row4.prop(self, "filter4_colorspace", text='')
		row4.prop(self, "filter4_alphamode", text='')
		
		grid.prop(self, "filter5_name", text='')
		row5 = grid.row(align=False)
		if not bpy.context.preferences.addons['VF_updateImages'].preferences.filter5_name:
			row5.enabled = False
		row5.prop(self, "filter5_colorspace", text='')
		row5.prop(self, "filter5_alphamode", text='')

###########################################################################
# Individual project settings
		
class UpdateImagesSettings(bpy.types.PropertyGroup):
	file_extension_source: bpy.props.StringProperty(
		name="Source File Extension",
		description="Define the file extension you want to replace",
		default=".png",
		maxlen=4096)
	file_extension_target: bpy.props.StringProperty(
		name="Target File Extension",
		description="Replace all source file extensions with this file extension",
		default=".jpg",
		maxlen=4096)

###########################################################################
# Display in Node panel

class IMAGE_PT_update_images_display(bpy.types.Panel):
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'UI'
	bl_category = "Node"
	bl_label = "Update Images"
#	bl_parent_id = "NODE_PT_active_node_properties"
#	bl_options = {'HIDE_HEADER'}
	
	def draw(self, context):
		layout = self.layout
		layout.use_property_decorate = False  # No animation
		layout.use_property_split = True

		# Update all images
		if bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_reload and bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_format:
			update_text = 'Update All Images'
		elif bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_reload:
			update_text = 'Reload All Images'
		elif bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_format:
			update_text = 'Format All Images'
		if bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_reload or bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_format:
			ops = layout.operator(VF_Update_Images.bl_idname, text=update_text, icon='RENDERLAYERS')
			ops.reload = bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_reload
			ops.format = bpy.context.preferences.addons['VF_updateImages'].preferences.enable_file_format

		# Display source and target file extensions
		row = layout.row(align=True)
#		grid = row.grid_flow(columns=3, align=True)
		row.prop(context.scene.vf_update_images_settings, 'file_extension_source', text='')
		row.operator(VF_Switch_Extension_Settings.bl_idname, text='', icon='FILE_REFRESH')
		row.prop(context.scene.vf_update_images_settings, 'file_extension_target', text='')
		row.operator(VF_Replace_Image_Extensions.bl_idname, text='Replace')

###########################################################################
# Display in Image menu

def vf_update_images_button(self, context):
	self.layout.separator()
	self.layout.operator(VF_Update_Images.bl_idname)

###########################################################################
# Addon registration functions

classes = (VF_Update_Images, VF_Switch_Extension_Settings, VF_Replace_Image_Extensions, UpdateImagesPreferences, UpdateImagesSettings, IMAGE_PT_update_images_display)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Scene.vf_update_images_settings = bpy.props.PointerProperty(type=UpdateImagesSettings)
#	bpy.types.IMAGE_MT_editor_menus.append(vf_update_images_button)
	bpy.types.IMAGE_MT_image.append(vf_update_images_button)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
	del bpy.types.Scene.vf_update_images_settings
#	bpy.types.IMAGE_MT_editor_menus.remove(vf_update_images_button)
	bpy.types.IMAGE_MT_image.remove(vf_update_images_button)

if __name__ == "__main__":
	register()