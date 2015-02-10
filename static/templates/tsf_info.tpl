<dl class="dl-horizontal">
	<dt>Nom de la tache :</dt>
	<dd>{{headers.JobName}}</dd>
	
	<dt>Nom du fichier :</dt>
	<dd>{{filename}}</dd>

	<dt>Date de création :</dt>
	<dd>{{date date "DD/MM/YYYY à HH:mm"}}</dd>

	<dt>Taille du fichier :</dt>
	<dd>{{numeral weight "0.0b"}}</dd>

	<dt>Dimensions de la tache :</dt>
	<dd>
		<strong>{{numeral headers.Size.width "0,0.0"}}</strong>&thinsp;x&thinsp;<strong>{{numeral headers.Size.height "0,0.0"}}</strong> mm <em>({{numeral headers.px_width "0,0"}}&thinsp;x&thinsp;{{numeral headers.px_height "0,0"}} px)</em>
	</dd>

	<dt>Résolution :</dt>
	<dd>{{#when headers.Resolution gt=500}}
		<strong class="text-warning">{{headers.Resolution}}dpi <i class="fa fa-exclamation-triangle" title="La resolution est très elevée"></i></strong>
	{{else}}
		{{headers.Resolution}}dpi
	{{/when}}</dd>

	<dt>Type de gravure :</dt>
	<dd>
		{{#if headers.bmp}} 
			 
			{{#when headers.ProcessMode equals='Layer'}}
				Couches : <em>({{headers.LayerParameter.layers}} couches, ajustement de {{numeral headers.LayerParameter.adjustment "0.000"}} mm)</em>
			{{/when}}
			{{#when headers.ProcessMode equals='Stamp'}}
				Tampon : <em>({{headers.StampShoulder}})</em>
			{{/when}}
			{{#when headers.ProcessMode equals='Standard'}}
				Standard
			{{/when}}
			{{#when headers.ProcessMode equals='Relief'}}
				Relief
			{{/when}}
		{{else}} 
			<i class="fa fa-ban text-danger"></i> Aucune gravure
		{{/if}}
	</dd>
	
	<dt>Découpe : </dt>
	<dd>
		{{#if headers.cut}} 
			{{#each headers.cut}}
				<div class="colorbox" style="background-color:{{this}}" title="{{this}}">&nbsp;</div>
			{{/each}}
		{{else}} 
			<i class="fa fa-ban text-danger"></i> Aucune découpe
		{{/if}}
	
	</dd>
</dl>
