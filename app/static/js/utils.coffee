class Utils
    uiBind: (scope, dependencies)=>
        if typeof dependencies isnt 'object'
            throw TypeError('Dependencies have to be passed as object')
            dependencies = [dependencies]
        for dep in dependencies
            console.log dep



angular.module('arte-ww.utils').service('utils', Utils)